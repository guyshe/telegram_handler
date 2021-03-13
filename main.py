import logging

from telegram_handler import AsyncTelegramHandler

BOT_TOKEN = '<bot-token>'
CHANNEL_NAME = '<channel-name>'


def main():
    telegram_log_handler = AsyncTelegramHandler(BOT_TOKEN, CHANNEL_NAME)
    my_logger = logging.getLogger('My-Logger')
    my_logger.setLevel(logging.INFO)
    my_logger.addHandler(logging.StreamHandler())
    my_logger.addHandler(telegram_log_handler)

    for i in range(5):
        my_logger.error(f'iterating {i}..')


if __name__ == '__main__':
    main()
