FLUSH_INTERVAL = 5

API_HOST = "api.telegram.org"
API_FORMAT_REQUEST = f"https://{API_HOST}/bot{{bot_token}}"
API_SEND_MESSAGE_REQUEST = (
    "{api_request}/sendMessage?chat_id={channel_name}&parse_mode=HTML"
)
API_VALIDATE_TOKEN_REQUEST = "{api_request}/getMe"
API_VALIDATE_CHAT_REQUEST = "{api_request}/getChat?chat_id={channel_name}"
RETRY_COOLDOWN_TIME = 60
MAX_RETRYS = 20
RETRY_BACKOFF_TIME = 5
# max valid size is 4096, we take margin to be on the safe side
MAX_MESSAGE_SIZE = 4000
TOO_MANY_REQUESTS = 429
MAX_BUFFER_SIZE = 10**16
