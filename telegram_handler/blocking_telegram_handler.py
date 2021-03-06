import logging

import requests
from requests import HTTPError
from telegram_handler.functools_extension import retry
from telegram_handler.consts import API_URL, COOLDOWN_TIME, \
    NEED_COOLDOWN_STATUS, RETRY_ATTEMPTS


def _is_cooldown_exception(exception: Exception):
    return (isinstance(exception, HTTPError)) and \
           (NEED_COOLDOWN_STATUS == exception.response.status_code)


class BlockingTelegramHandler(logging.Handler):

    def __init__(self, bot_token, channel_name):
        super().__init__()
        self.bot_token = bot_token
        self.channel_name = channel_name

    @retry(_is_cooldown_exception, RETRY_ATTEMPTS, COOLDOWN_TIME)
    def emit(self, record: logging.LogRecord) -> None:
        url = API_URL.format(
            bot_token=self.bot_token,
            channel_name=self.channel_name,
            message=record.getMessage()
        )
        requests.get(url).raise_for_status()
