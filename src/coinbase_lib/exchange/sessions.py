# -*- coding: UTF-8 -*-

from .authentication import SessionAuth
from ..sessions import BaseSession

__all__ = ["AuthSession"]


class AuthSession(BaseSession):
    """Coinbase authenticated session."""

    def __init__(self, key: str, passphrase: str, secret: str, **kwargs):
        """
        :param key: The API key.
        :param passphrase: The API passphrase.
        :param secret: The API secret.
        :param kwargs: Additional keyword arguments.
        """
        super(AuthSession, self).__init__(**kwargs)
        self.auth = SessionAuth(key, passphrase, secret)
