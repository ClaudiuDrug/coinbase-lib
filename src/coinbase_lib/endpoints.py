# -*- coding: UTF-8 -*-

from abc import ABC

from requests import Session, Response

from .helpers import URL


class Endpoint(ABC):
    """Base endpoint for all handlers in this module."""

    _url: URL = None
    _session: Session = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def _request(self, method, *args, **kwargs) -> Response:
        url: str = self._url.join(*args)
        kwargs.update(url=url)

        response: Response = method(**kwargs)

        if response.status_code != 200:
            response.raise_for_status()

        return response

    def _get(self, *args, **kwargs) -> Response:
        """Send a `GET` request and return the response."""
        return self._request(self._session.get, *args, **kwargs)

    def _post(self, *args, **kwargs) -> Response:
        """Send a `POST` request and return the response."""
        return self._request(self._session.post, *args, **kwargs)

    def _delete(self, *args, **kwargs) -> Response:
        """Send a `DELETE` request and return the response."""
        return self._request(self._session.delete, *args, **kwargs)

    def _put(self, *args, **kwargs) -> Response:
        """Send a `PUT` request and return the response."""
        return self._request(self._session.put, *args, **kwargs)

    def close(self):
        """Close the session handler."""
        self._session.close()
