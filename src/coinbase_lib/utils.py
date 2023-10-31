# -*- coding: UTF-8 -*-

from datetime import datetime, timezone
from logging import getLogger, Logger, StreamHandler, Formatter
from typing import Union, Any

from requests import Response
from requests_toolbelt.utils import dump


def decode(value: Union[bytes, str], **kwargs) -> str:
    """
    Decode the bytes using the codec registered for encoding.

    :param value: Value to be decoded.
    :param kwargs: Additional keyword arguments.
    """
    if isinstance(value, bytes):
        return value.decode(**kwargs)
    return value


def encode(value: Union[str, bytes], **kwargs) -> bytes:
    """
    Encode the string using the codec registered for encoding.

    :param value: Value to be encoded.
    :param kwargs: Additional keyword arguments.
    """
    if isinstance(value, str):
        return value.encode(**kwargs)
    return value


def get_posix() -> float:
    """
    POSIX timestamp as float.
    Number of seconds since Unix Epoch in UTC.
    """
    utc = get_utc()
    return utc.timestamp()


def get_utc() -> datetime:
    """UTC as `datetime` object."""
    return datetime.now(timezone.utc)


def extract_msg(response: Response, **kwargs) -> str:
    """
    Dump all requests and responses including redirects.
    This takes the response returned by requests and will dump all
    request-response pairs in the redirect history in order followed by the
    final request-response.

    :param response: The response returned by requests.
    :param kwargs: Additional keyword arguments.
    """
    return decode(
        dump.dump_all(response),
        **kwargs
    )


def get_logger(name: str, level: int, fmt: str) -> Logger:
    """
    Create and return a logger instance that outputs messages to console.
    """
    # create a logger and set level to debug:
    logger: Logger = getLogger(name)
    logger.setLevel(level)

    # create console handler and set ths level:
    handler = StreamHandler()
    handler.setLevel(level)

    # create formatter:
    formatter = Formatter(fmt)

    # add formatter to console:
    handler.setFormatter(formatter)

    # add console to logger:
    logger.addHandler(handler)
    return logger


def as_str(value: Any) -> str:
    """
    Convert any given `value` to `str`.

    :param value: Value to be converted.
    """
    if not isinstance(value, str):
        return str(value)
    return value
