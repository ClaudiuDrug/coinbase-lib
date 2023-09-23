# -*- coding: UTF-8 -*-

from os.path import join

from ..constants import ROOT

__all__ = ["NAME", "ENVIRONMENT", "CACHE"]

# instance name:
NAME: str = "exchange"

# hostname environment:
ENVIRONMENT: str = "production"  # or: "sandbox"

# cache settings:
CACHE: dict = {
    "name": join(ROOT, "cache", NAME),
    "backend": "sqlite",
    "expire": 180,
}
