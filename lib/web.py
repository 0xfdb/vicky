from dataclasses import dataclass
from typing import Any, Optional

import requests


# TODO consider better handling of this
@dataclass
class Request:
    status: int
    "http status code"
    url: str
    "url"
    data: Any
    "whatever was returned from the request, including None"


class Web:
    """
    Smol wrapper for requests.Session()
    """

    # TODO proxy support
    def __init__(self, headers: Optional[dict] = None, timeout: Optional[int] = 5):
        self.client = httpx.Client()
        if headers:
            self.client.headers.update(headers)
        self.timeout = timeout


def get(
    url: str,
    session: Optional[Web] = None,
    json: bool = False,
    **kwargs: Optional[dict],
) -> Request:
    """
    HTTP GET with requests
    returns Request object
    """
    if session is not None:
        req = session.client.get(url=url, timeout=session.timeout)
    else:
        req = httpx.get(url=url, **kwargs)

    status = req.status_code
    if json:
        return Request(status, str(req.url), req.json())
    else:
        return Request(status, str(req.url), req.text)


def post(url: str, data: dict, session: Optional[Web] = None) -> Request:
    """
    HTTP POST with requests
    returns Request object
    """
    if session is not None:
        session.client.post(url=url, data=data, timeout=session.timeout)
    else:
        req = httpx.post(url=url, data=data)
    return Request(req.status_code, url, req.text)

