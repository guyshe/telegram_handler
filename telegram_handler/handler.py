from distutils.log import Log
import logging
from time import sleep
from threading import Thread, RLock
from queue import Empty, Queue
import requests
from retry import retry
from telegram_handler.consts import API_URL, RETRY_COOLDOWN_TIME, MAX_RETRYS, MAX_MESSAGE_SIZE, FLUSH_INTERVAL

logger = logging.getLogger(__name__)


class TelegramLoggingHandler(logging.Handler):

    _sentinel = None

    def __init__(self, bot_token, channel_name, level=logging.NOTSET):
        super().__init__(level)
        self.bot_token = bot_token
        self.channel_name = channel_name
        self._buffer_lock = RLock()
        self._buffer = ''
        self.telegram_messages_queue = Queue()
        self._writer_thread = None
        self._start_writer_thread()

    @retry(requests.RequestException,
           tries=MAX_RETRYS,
           delay=RETRY_COOLDOWN_TIME,
           logger=logger)
    def write(self, message):
        url = API_URL.format(bot_token=self.bot_token,
                             channel_name=self.channel_name)
        requests.post(url, data={'text': message}).raise_for_status()

    def emit(self, record: logging.LogRecord) -> None:
        message = self.format(record)
        self._buffer_lock.acquire()
        new_buffer = f'{self._buffer}\n{message}'
        if len(new_buffer) > MAX_MESSAGE_SIZE:
            self._flush_buffer()
            new_buffer = message[:MAX_MESSAGE_SIZE]
        self._buffer = new_buffer
        self._buffer_lock.release()

    def close(self):
        self._flush_buffer()
        self.telegram_messages_queue.put(TelegramLoggingHandler._sentinel)
        self.telegram_messages_queue.join()
        self._writer_thread.join()

    def _flush_buffer(self):
        self._buffer_lock.acquire()
        # Avoid unnecessary flushing
        if self._buffer != '':
            self.telegram_messages_queue.put(self._buffer[:MAX_MESSAGE_SIZE])
            self._buffer = ''
        self._buffer_lock.release()

    def _write_manager(self):
        q = self.telegram_messages_queue
        while True:
            try:
                message = q.get(timeout=FLUSH_INTERVAL)
                if message is self._sentinel:
                    q.task_done()
                    break
                self.write(message)
                q.task_done()
            except Empty:
                self._flush_buffer()
            except Exception:
                logging.exception('Got exception while handling log')

    def _start_writer_thread(self):
        self._writer_thread = Thread(target=self._write_manager)
        self._writer_thread.daemon = True
        self._writer_thread.start()
