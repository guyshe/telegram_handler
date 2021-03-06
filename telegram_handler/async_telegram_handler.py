import logging
from queue import Queue
from logging.handlers import QueueHandler, QueueListener

from telegram_handler.blocking_telegram_handler import BlockingTelegramHandler


class AsyncTelegramHandler(logging.Handler):
    def __init__(self, bot_token, channel_name):
        super().__init__()
        self._blocking_handler = BlockingTelegramHandler(
            bot_token,
            channel_name
        )
        self._queue = Queue()
        self._queue_handler = QueueHandler(self._queue)
        self._queue_listener = QueueListener(
            self._queue,
            self._blocking_handler
        )
        self._start()

    def emit(self, record: logging.LogRecord) -> None:
        self._queue_handler.emit(record)

    def _start(self):
        self._queue_listener.start()

    def _stop(self):
        self._queue_listener.stop()

    def close(self):
        self._stop()
        super().close()

    def setFormatter(self, fmt: logging.Formatter) -> None:
        self._queue_handler.setFormatter(fmt)
        super().setFormatter(fmt)
