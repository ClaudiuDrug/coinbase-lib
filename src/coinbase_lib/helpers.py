# -*- coding: UTF-8 -*-

from dataclasses import dataclass, field
from typing import List

from .utils import as_str


@dataclass
class URL:
    """URL path constructor."""

    hostname: str
    protocol: str = field(default="https")
    port: int = field(default=None)
    base_path: str = field(default=None)
    endpoint: str = field(default=None)

    @property
    def path(self) -> str:
        path: str = f"{self.protocol}://{self.hostname}"

        if self.port is not None:
            path = f"{path}:{self.port}"

        if self.base_path is not None:
            path = f"{path}/{self.base_path}"

        if self.endpoint is not None:
            return f"{path}/{self.endpoint}"

        return path

    def join(self, *args, **kwargs) -> str:
        """
        Construct an url address using `args` for path and `kwargs` as
        query params if given.
        """
        if len(args) > 0:
            args: List[str] = [as_str(arg) for arg in args]

        path: str = "/".join(args)

        if len(kwargs) > 0:
            params: List[str] = [f"{key}={value}" for key, value in kwargs.items()]
            path = f"{path}?{'&'.join(params)}"

        if len(path) > 0:
            return f"{self.path}/{path}"

        return self.path

    def __str__(self) -> str:
        return self.path
