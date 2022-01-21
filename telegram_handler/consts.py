FLUSH_INTERVAL = 0.5

API_HOST = 'api.telegram.org'
API_URL = f'https://{API_HOST}/bot{{bot_token}}/sendMessage?' \
          f'chat_id=@{{channel_name}}&parse_mode=HTML&text={{message}}'
RETRY_COOLDOWN_TIME = 3
MAX_RETRYS = 20
# max valid size is 2048, we take buffer to be on the safe side
MAX_MESSAGE_SIZE = 1900
MAX_TELEGRAM_MESSAGES = 300
