from typing import Optional
from threading import RLock


class MessageBuffer:
    def __init__(self, max_size: Optional[int] = None):
        self._lock = RLock()
        self._buffer = ""
        self._max_size = max_size

    def write(self, message: str):
        with self._lock:
            self._buffer = "".join([self._buffer, message])[: self._max_size]

    def read(self, count: int):
        result = ""
        with self._lock:
            result, self._buffer = self._buffer[:count], self._buffer[count:]
        return result
