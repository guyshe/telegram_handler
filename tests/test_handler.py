from telegram_handler.consts import API_HOST
from telegram_handler import TelegramLoggingHandler

BOT_TOKEN = 'FAKE_BOT_TOKEN'
CHANNEL_NAME = 'FAKE_CHANNEL_NAME'
CHAT_ID = 123456


def test_format_url_channel_name():
    handler = TelegramLoggingHandler(BOT_TOKEN, CHANNEL_NAME)
    assert handler._url == f'https://{API_HOST}/bot{BOT_TOKEN}/sendMessage?' \
          f'chat_id=@{CHANNEL_NAME}&parse_mode=HTML'


def test_format_url_chat_id():
    handler = TelegramLoggingHandler(BOT_TOKEN, CHAT_ID)
    assert handler._url == f'https://{API_HOST}/bot{BOT_TOKEN}/sendMessage?' \
          f'chat_id={CHAT_ID}&parse_mode=HTML'