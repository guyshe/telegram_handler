# Telegram Handler
Drop-in Python `logging.Handler` that forwards log records to a Telegram chat or channel with buffering, retries, and a background worker so your app stays responsive.

## Highlights
- Works with channel usernames or chat IDs; just pass your bot token and destination.
- Buffered writer batches messages and trims overlong payloads to avoid Telegram limits.
- Automatic retries with backoff when Telegram throttles or transient network errors occur.
- Thread-safe background thread keeps log emission non-blocking for the main application.
- Simple to slot into existing logging setups alongside stream/file handlers.

## Install
```bash
pip install telegram-handler
```

## Quickstart
```python
import logging

from telegram_handler import TelegramLoggingHandler

BOT_TOKEN = "123456:ABCDEF_example_bot_token"
CHANNEL = "example_channel_logger"  # or an integer chat ID

handler = TelegramLoggingHandler(BOT_TOKEN, CHANNEL)
logging.basicConfig(
    handlers=[handler, logging.StreamHandler()],
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)

logger = logging.getLogger("demo")
for i in range(5):
    logger.error("iterating %s..", i)
```

## What you need
- Create a bot with [BotFather](https://core.telegram.org/bots#3-how-do-i-create-a-bot) to obtain `BOT_TOKEN`.
- Create a channel or use a chat; add your bot as an admin so it can post messages.
- Find the chat ID if you prefer using IDs instead of a public channel name (guide [here](http://techblog.sillifish.co.uk/2020/03/30/telegram-chat-id-and-token-id/)).

## Usage notes
- `bot_token`: token returned by BotFather (keep it secret; do not commit it).
- `channel`: public channel username (without the leading `@`) or an integer chat ID.
- Messages are buffered and flushed every few seconds in a daemon thread to keep logging non-blocking.
- Payloads are trimmed to stay under Telegram's message size limits; long bursts are split across flushes.
- The handler automatically retries with exponential backoff on Telegram's `429 Too Many Requests` responses.
- Call `handler.close()` during shutdown if you need to stop the background thread cleanly.

## Screenshot
![screenshot](https://github.com/guyshe/telegram_handler/blob/master/screenshot.png?raw=true)

## Development
- Run tests: `tox`
- Lint with ruff: `ruff check`
