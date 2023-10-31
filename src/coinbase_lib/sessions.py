# -*- coding: UTF-8 -*-

from logging import Logger, getLogger

from requests import Session, Response
from requests.adapters import HTTPAdapter
from requests_cache import install_cache
from urllib3.util.retry import Retry

from .constants import CACHE, HEADERS, NAME
from .utils import extract_msg


class TimeoutHTTPAdapter(HTTPAdapter):
    """Custom HTTP adapter with timeout capability."""

    def __init__(self, retries: int = 3, backoff: float = 1, timeout: int = 30):
        self._timeout = timeout
        max_retries = Retry(
            total=retries,
            backoff_factor=backoff
        )
        super(TimeoutHTTPAdapter, self).__init__(max_retries=max_retries)

    def send(self, request, **kwargs):
        return super(TimeoutHTTPAdapter, self).send(request, timeout=self._timeout, **kwargs)


class BaseSession(Session):
    """Base `Session`."""

    _log: Logger = getLogger(NAME)

    def __init__(
            self,
            retries: int = 3,
            backoff: int = 1,
            timeout: int = 30,
            cache: bool = True,
            debug: bool = False,
            logger: Logger = None
    ):
        """
        :param retries: Total number of retries to allow (defaults to: 3).
        :param backoff: A backoff factor to apply between attempts after the
            second try (defaults to: 1).
        :param timeout: How long to wait for the server to send data before
            giving up (defaults to: 30).
        :param cache: Use caching (defaults to: `True`);
        :param debug: Set to True to log all requests/responses to/from server
            (defaults to: `False`).
        :param logger: The handler to be used for logging. If given, and level
            is above `DEBUG`, all debug messages will be ignored.
        """
        if cache is True:
            install_cache(
                cache_name=CACHE.NAME,
                backend=CACHE.BACKEND,
                expire_after=CACHE.EXPIRE
            )

        if logger is not None:
            self._log = logger

        super(BaseSession, self).__init__()

        self.headers.update(HEADERS)

        self.mount(
            "http://",
            TimeoutHTTPAdapter(retries, backoff, timeout)
        )

        self.mount(
            "https://",
            TimeoutHTTPAdapter(retries, backoff, timeout)
        )

        if debug is True:
            self.hooks["response"] = [self.debug]

    def debug(self, response: Response, *args, **kwargs):
        message: str = extract_msg(response)
        self._log.debug(message)
