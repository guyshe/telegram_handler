from typing import Union
import logging
from time import sleep
import requests
from threading import Thread, RLock
from retry import retry
from telegram_handler.buffer import MessageBuffer
from telegram_handler.consts import (
    API_FORMAT_REQUEST,
    API_VALIDATE_CHAT_REQUEST,
    API_VALIDATE_TOKEN_REQUEST,
    API_SEND_MESSAGE_REQUEST,
    RETRY_COOLDOWN_TIME,
    MAX_RETRYS,
    MAX_MESSAGE_SIZE,
    FLUSH_INTERVAL,
    RETRY_BACKOFF_TIME,
    MAX_BUFFER_SIZE,
)
from telegram_handler.errors import (
    TelegramConfigurationError,
    TelegramUnexpectedResponseError,
)

logger = logging.getLogger(__name__)


class TelegramLoggingHandler(logging.Handler):
    def __init__(self, bot_token: str, channel: Union[str, int], level=logging.NOTSET):
        super().__init__(level)
        self._buffer = MessageBuffer(MAX_BUFFER_SIZE)
        self._stop_signal = RLock()
        self._writer_thread = None
        self._bot_token = bot_token
        self._channel = TelegramLoggingHandler._format_channel(channel)
        self._api_request_base = TelegramLoggingHandler._format_api(bot_token)
        self._validate_configuration()
        self._start_writer_thread()

    def _validate_configuration(self):
        self._validate_bot_token()
        self._validate_channel()

    def _validate_bot_token(self):
        url = API_VALIDATE_TOKEN_REQUEST.format(api_request=self._api_request_base)
        response = requests.get(url)
        self._validate_api_response(response)

    def _validate_channel(self):
        url = API_VALIDATE_CHAT_REQUEST.format(
            api_request=self._api_request_base, channel_name=self._channel
        )
        response = requests.get(url)
        self._validate_api_response(response)

    @staticmethod
    def _format_api(bot_token: str):
        return API_FORMAT_REQUEST.format(bot_token=bot_token)

    @staticmethod
    def _format_channel(channel: Union[str, int]):
        if isinstance(channel, str) and not channel.startswith("@"):
            return f"@{channel}"
        # In case of integer channel (chat id) or already formatted string
        return f"{channel}"

    @retry(
        requests.exceptions.RequestException,
        tries=MAX_RETRYS,
        delay=RETRY_COOLDOWN_TIME,
        backoff=RETRY_BACKOFF_TIME,
        logger=logger,
    )
    def write(self, message):
        url = API_SEND_MESSAGE_REQUEST.format(
            api_request=self._api_request_base, channel_name=self._channel
        )
        response = requests.post(url, data={"text": message})
        self._validate_api_response(response)

    def _validate_api_response(self, response: requests.Response):
        if response.ok:
            return
        if response.status_code == 401:
            raise TelegramConfigurationError("Unauthorized: Probably invalid bot token")
        try:
            response_data = response.json()
        except requests.exceptions.JSONDecodeError:
            raise TelegramUnexpectedResponseError(
                "Invalid JSON response from Telegram API"
            )
        if response.status_code == 400:
            raise TelegramConfigurationError(
                f"Bad Request: {response_data.get('description', 'Could not get description')}"
            )
        if response.status_code == 404:
            raise TelegramConfigurationError(
                "Not Found: The requested resource could not be found, this may happen if the bot token is invalid, or the api has changed"
            )
        response.raise_for_status()
        if response.status_code == requests.codes.too_many_requests:
            raise requests.exceptions.RequestException("Too many requests")

    def emit(self, record: logging.LogRecord) -> None:
        message = self.format(record)
        self._buffer.write(f"{message}\n")

    def close(self):
        with self._stop_signal:
            if self._writer_thread is None:
                return
            self._writer_thread.join()

    def _write_manager(self):
        while True:
            # as long as we can aquire the lock, we can continue
            lock_status = self._stop_signal.acquire(blocking=False)
            if not lock_status:
                break
            else:
                self._stop_signal.release()

            sleep(FLUSH_INTERVAL)
            message = self._buffer.read(MAX_MESSAGE_SIZE)
            if message != "":
                self.write(message)

    def _start_writer_thread(self):
        self._writer_thread = Thread(target=self._write_manager)
        self._writer_thread.daemon = True
        self._writer_thread.start()
