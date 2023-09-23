# -*- coding: UTF-8 -*-

from os.path import dirname, realpath
from sys import modules
from types import ModuleType

__all__ = [
    "NAME", "ENCODING", "MODULE", "ROOT", "RETRIES",
    "BACKOFF", "TIMEOUT", "HEADERS", "DEBUGGING", "FMT"
]

# instance name:
NAME: str = "coinbase-lib"

# global encoding:
ENCODING: str = "UTF-8"

# main module:
MODULE: ModuleType = modules.get("__main__")

# root directory:
ROOT: str = dirname(realpath(MODULE.__file__))

# http adapter settings:
RETRIES: int = 3
BACKOFF: int = 1
TIMEOUT: int = 30

# default headers:
HEADERS: dict = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "Accept-Charset": ENCODING,
}

# logger settings:
DEBUGGING: bool = False
FMT: str = "[%(asctime)s] - %(levelname)s - <%(filename)s, %(lineno)d, %(funcName)s>: %(message)s"
