import requests
import pytest

from telegram_handler.consts import API_FORMAT_REQUEST, API_SEND_MESSAGE_REQUEST
from telegram_handler import TelegramLoggingHandler
from telegram_handler.errors import TelegramConfigurationError

BOT_TOKEN = "FAKE_BOT_TOKEN"
INVALID_FORMAT_BOT_TOKEN = "12345678999:ABCDzA-abcd9Pgd49_hj_OT5T40lsU5-UUcP"
CHANNEL_NAME = "FAKE_CHANNEL_NAME"
CHAT_ID = 123456


class DummyResponse:
    ok = True
    status_code = 200

    def json(self):
        return {}


class DummyUnauthorizedResponse:
    ok = False
    status_code = 401


class DummyNotFoundResponse:
    ok = False
    status_code = 404

    def json(self):
        return {}


class DummyBadRequestResponse:
    ok = False
    status_code = 400

    def json(self):
        return {"description": "Bad Request: chat not found"}


def test_format_url_channel_name(monkeypatch):
    monkeypatch.setattr(requests, "get", lambda *args, **kwargs: DummyResponse())
    monkeypatch.setattr(
        TelegramLoggingHandler, "_start_writer_thread", lambda self: None
    )
    handler = TelegramLoggingHandler(BOT_TOKEN, CHANNEL_NAME)
    assert handler._channel == f"@{CHANNEL_NAME}"
    assert handler._api_request_base == API_FORMAT_REQUEST.format(bot_token=BOT_TOKEN)
    expected_url = API_SEND_MESSAGE_REQUEST.format(
        api_request=handler._api_request_base, channel_name=handler._channel
    )
    assert expected_url == (
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?"
        f"chat_id=@{CHANNEL_NAME}&parse_mode=HTML"
    )


def test_format_url_chat_id(monkeypatch):
    monkeypatch.setattr(requests, "get", lambda *args, **kwargs: DummyResponse())
    monkeypatch.setattr(
        TelegramLoggingHandler, "_start_writer_thread", lambda self: None
    )
    handler = TelegramLoggingHandler(BOT_TOKEN, CHAT_ID)
    assert handler._channel == f"{CHAT_ID}"
    assert handler._api_request_base == API_FORMAT_REQUEST.format(bot_token=BOT_TOKEN)
    expected_url = API_SEND_MESSAGE_REQUEST.format(
        api_request=handler._api_request_base, channel_name=handler._channel
    )
    assert expected_url == (
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?"
        f"chat_id={CHAT_ID}&parse_mode=HTML"
    )


def test_invalid_token_unauthorized(monkeypatch):
    monkeypatch.setattr(
        requests, "get", lambda *args, **kwargs: DummyUnauthorizedResponse()
    )
    monkeypatch.setattr(
        TelegramLoggingHandler, "_start_writer_thread", lambda self: None
    )
    with pytest.raises(
        TelegramConfigurationError, match="Unauthorized: Probably invalid bot token"
    ):
        TelegramLoggingHandler(INVALID_FORMAT_BOT_TOKEN, CHANNEL_NAME)


def test_fake_token_not_found(monkeypatch):
    monkeypatch.setattr(
        requests, "get", lambda *args, **kwargs: DummyNotFoundResponse()
    )
    monkeypatch.setattr(
        TelegramLoggingHandler, "_start_writer_thread", lambda self: None
    )
    with pytest.raises(
        TelegramConfigurationError,
        match=(
            "Not Found: The requested resource could not be found, this may happen if "
            "the bot token is invalid, or the api has changed"
        ),
    ):
        TelegramLoggingHandler(BOT_TOKEN, CHANNEL_NAME)


def test_invalid_channel_bad_request(monkeypatch):
    responses = [DummyResponse(), DummyBadRequestResponse()]

    def fake_get(*args, **kwargs):
        return responses.pop(0)

    monkeypatch.setattr(requests, "get", fake_get)
    monkeypatch.setattr(
        TelegramLoggingHandler, "_start_writer_thread", lambda self: None
    )
    with pytest.raises(
        TelegramConfigurationError, match="Bad Request: .*chat not found"
    ):
        TelegramLoggingHandler(BOT_TOKEN, CHANNEL_NAME)


def test_write_sends_expected_request(monkeypatch):
    captured = {}

    def fake_post(url, data=None, **kwargs):
        captured["url"] = url
        captured["data"] = data
        return DummyResponse()

    monkeypatch.setattr(requests, "get", lambda *args, **kwargs: DummyResponse())
    monkeypatch.setattr(requests, "post", fake_post)
    monkeypatch.setattr(
        TelegramLoggingHandler, "_start_writer_thread", lambda self: None
    )
    handler = TelegramLoggingHandler(BOT_TOKEN, CHANNEL_NAME)
    handler.write("hello")

    expected_url = API_SEND_MESSAGE_REQUEST.format(
        api_request=API_FORMAT_REQUEST.format(bot_token=BOT_TOKEN),
        channel_name=f"@{CHANNEL_NAME}",
    )
    assert captured["url"] == expected_url
    assert captured["data"] == {"text": "hello"}
