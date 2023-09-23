# -*- coding: UTF-8 -*-

from datetime import datetime, timezone
from logging import Logger, getLogger, StreamHandler, Formatter
from typing import Union

__all__ = ["decode", "encode", "get_posix", "get_utc", "get_logger"]


def decode(value: Union[bytes, str], **kwargs) -> str:
    """
    Decode the bytes value using the codec registered for encoding.

    :param value: Value to be decoded.
    :param kwargs: Additional keyword arguments.
    :return: Decoded string.
    """
    if isinstance(value, bytes):
        return value.decode(**kwargs)
    return value


def encode(value: Union[str, bytes], **kwargs) -> bytes:
    """
    Encode the string value using the codec registered for encoding.

    :param value: Value to be encoded.
    :param kwargs: Additional keyword arguments.
    :return: Encoded string.
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


def get_logger(name: str, level: int, fmt: str) -> Logger:
    """
    Create a logger and with severity level `DEBUG`.

    :param name: Instance name.
    :param level: Severity level.
    :param fmt: Log message format.
    :return: A logger instance.
    """
    logger: Logger = getLogger(name)
    logger.setLevel(level)

    # create console handler and set level to debug:
    handler = StreamHandler()
    handler.setLevel(level)

    # create formatter:
    formatter = Formatter(fmt)

    # add formatter to console:
    handler.setFormatter(formatter)

    # add console to logger:
    logger.addHandler(handler)
    return logger
