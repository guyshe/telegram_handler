import logging

from telegram_handler import AsyncTelegramHandler

BOT_TOKEN = '1687808712:AAGcV2SxriHSCBg1zYC3STiyIuFBTO7xYfQ'
CHANNEL_NAME = 'guysheloggerchannel'


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
