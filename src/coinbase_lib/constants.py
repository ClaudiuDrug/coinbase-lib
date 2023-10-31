# -*- coding: UTF-8 -*-

from os.path import dirname, realpath, join
from sys import modules
from types import ModuleType

# instance name:
NAME: str = "coinbase"

# main module:
MODULE: ModuleType = modules.get("__main__")

# root directory:
ROOT: str = dirname(realpath(MODULE.__file__))

# default encoding:
ENCODING: str = "UTF-8"

# logging fmt:
FMT: str = "[%(asctime)s] - %(levelname)s - <%(filename)s, %(lineno)d, %(funcName)s>: %(message)s"

# default headers
HEADERS: dict = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "Accept-Charset": "utf-8",
}


class CACHE:
    """Cache settings."""
    NAME: str = join(ROOT, "cache", NAME),
    BACKEND: str = "sqlite",
    EXPIRE: int = 180
