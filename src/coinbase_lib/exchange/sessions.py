# -*- coding: UTF-8 -*-

from logging import Logger, DEBUG

from .authentication import SessionAuth
from .constants import NAME
from ..constants import FMT, RETRIES, BACKOFF, TIMEOUT, DEBUGGING
from ..sessions import BaseSession
from ..utils import get_logger

__all__ = ["AuthSession"]


class AuthSession(BaseSession):
    """Coinbase authenticated session."""

    _log = get_logger(NAME, level=DEBUG, fmt=FMT)

    def __init__(
            self,
            key: str,
            passphrase: str,
            secret: str,
            retries: int = RETRIES,
            backoff: int = BACKOFF,
            timeout: int = TIMEOUT,
            debug: bool = DEBUGGING,
            logger: Logger = None,
            cache: dict = None,
    ):
        """
        :param key: The API key.
        :param passphrase: The API passphrase.
        :param secret: The API secret.
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
        super(AuthSession, self).__init__(
            retries=retries,
            backoff=backoff,
            timeout=timeout,
            debug=debug,
            logger=logger,
            cache=cache,
        )
        self.auth = SessionAuth(key, passphrase, secret)
