class TelegramHandlerError(Exception):
    """Base class for all Telegram handler errors."""


class TelegramUnexpectedResponseError(TelegramHandlerError):
    """Raised when an unexpected error occurs in the Telegram handler."""


class TelegramConfigurationError(TelegramHandlerError):
    """Raised when Telegram rejects the configuration (chat or token)."""
