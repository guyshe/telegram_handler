API_HOST = 'api.telegram.org'
API_URL = f'https://{API_HOST}/bot{{bot_token}}/sendMessage?' \
          f'chat_id=@{{channel_name}}&text={{message}}'
NEED_COOLDOWN_STATUS = 429
COOLDOWN_TIME = 1
RETRY_ATTEMPTS = 6
