# -*- coding: UTF-8 -*-

from logging import Logger, DEBUG

from requests import Session, Response
from requests.adapters import HTTPAdapter
from requests_cache import install_cache
from requests_toolbelt.utils import dump
from urllib3.util.retry import Retry

from .constants import (
    NAME, FMT, RETRIES, BACKOFF, TIMEOUT,
    DEBUGGING, ENCODING, HEADERS
)
from .utils import decode, get_logger

__all__ = ["TimeoutHTTPAdapter", "BaseSession"]


class TimeoutHTTPAdapter(HTTPAdapter):
    """Custom HTTP adapter with timeout capability."""

    def __init__(self, *args, **kwargs):
        self._timeout = kwargs.pop("timeout")
        super(TimeoutHTTPAdapter, self).__init__(*args, **kwargs)

    def send(self, request, **kwargs):
        kwargs.update({"timeout": self._timeout})
        return super(TimeoutHTTPAdapter, self).send(request, **kwargs)


class BaseSession(Session):
    """Base `Session` handler."""

    _log = get_logger(NAME, level=DEBUG, fmt=FMT)

    @staticmethod
    def _http_adapter(retries: int, backoff: int, timeout: int) -> TimeoutHTTPAdapter:
        return TimeoutHTTPAdapter(
            max_retries=Retry(
                total=retries,
                backoff_factor=backoff
            ),
            timeout=timeout
        )

    @staticmethod
    def _extract_data(response: Response, **kwargs) -> str:
        return decode(
            dump.dump_all(response),
            **kwargs
        )

    @staticmethod
    def _install_cache(name: str, backend: str, expire: int):
        install_cache(
            cache_name=name,
            backend=backend,
            expire_after=expire
        )

    def __init__(
            self,
            retries: int = RETRIES,
            backoff: int = BACKOFF,
            timeout: int = TIMEOUT,
            debug: bool = DEBUGGING,
            logger: Logger = None,
            cache: dict = None,
    ):
        """
        :param retries: Total number of retries to allow.
        :param backoff: A backoff factor to apply between attempts after the
            second try.
        :param timeout: How long to wait for the server to send data before
            giving up.
        :param cache: A dictionary with `name`, `backend` and `expire` as keys.
        :param debug: Set to True to log all requests/responses to/from server.
        :param logger: The handler to be used for logging. If given, and level
            is above `DEBUG`, all debug messages will be ignored.
        """

        if cache is not None:
            self._install_cache(**cache)

        if logger is not None:
            self._log = logger

        super(BaseSession, self).__init__()

        self.headers.update(HEADERS)

        self.mount(
            "http://",
            self._http_adapter(retries, backoff, timeout)
        )

        self.mount(
            "https://",
            self._http_adapter(retries, backoff, timeout)
        )

        if debug is True:
            self.hooks["response"] = [self._debug]

    def _debug(self, response: Response, *args, **kwargs):
        self._log.debug(
            msg=self._extract_data(response, encoding=ENCODING, errors="ignore")
        )
