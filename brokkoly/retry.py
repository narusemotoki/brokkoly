import abc
import enum
from typing import Optional


RetryMethod = enum.Enum('RetryMethod', ['countdown'])  # type: ignore


class RetryPolicy(metaclass=abc.ABCMeta):
    @abc.abstractproperty
    def max_retries(self) -> Optional[int]:
        """If it returns None, use the default value.
        """
        ...

    @abc.abstractproperty  # type: ignore
    def retry_method(self) -> RetryMethod:
        ...

    @abc.abstractmethod
    def countdown(self, retry_count: int, error: Exception) -> int:
        ...


class CountdownPolicy(RetryPolicy):
    ...


class FibonacciBackoff(CountdownPolicy):
    """Wait for 1 second, 2 seconds, 3 seconds, 5 seconds ...
    """

    def __init__(self, max_retries: int, max_wait_seconds: int=None) -> None:
        """
        :param max_retries: Task gives up if process is failing after try this count.
        :param max_wait_seconds: countdown method doesn't return number greater than this numbers.
        """
        self._max_retries = max_retries
        self._max_wait_seconds = max_wait_seconds

    @property
    def max_retries(self) -> Optional[int]:
        return self._max_retries

    @property  # type: ignore
    def retry_method(self) -> RetryMethod:
        return RetryMethod.countdown  # type: ignore

    def countdown(self, retry_count: int, error: Exception) -> int:
        x, y = 1, 1
        for _ in range(retry_count):
            x, y = y, x + y
            if self._max_wait_seconds is not None and y >= self._max_wait_seconds:
                return self._max_wait_seconds
        return y


class ExponentialBackoff(CountdownPolicy):
    """Wait for 2 second, 4 seconds, 8 seconds, 16 seconds ...
    """

    def __init__(self, max_retries: int, max_wait_seconds: int=None) -> None:
        """
        :param max_retries: Task gives up if process is failing after try this count.
        :param max_wait_seconds: countdown method doesn't return number greater than this numbers.
        """
        self._max_retries = max_retries
        self._max_wait_seconds = max_wait_seconds

    @property
    def max_retries(self) -> Optional[int]:
        return self._max_retries

    @property  # type: ignore
    def retry_method(self) -> RetryMethod:
        return RetryMethod.countdown  # type: ignore

    def countdown(self, retry_count: int, error: Exception) -> int:
        wait = pow(2, retry_count + 1)
        return wait if self._max_wait_seconds < wait else self._max_wait_seconds
