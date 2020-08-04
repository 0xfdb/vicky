from dataclasses import dataclass
from typing import Any, Optional

import httpx


# TODO consider better handling of this
@dataclass
class Response:
    data: Any
    resobj: httpx.Response

    def __post_init__(self):
        self.url = str(self.resobj.url)
        self.status = self.resobj.status_code


class Web:
    """
    Smol wrapper for httpx.Client()
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
) -> Response:
    if session is not None:
        response = session.client.get(url=url, timeout=session.timeout)
    else:
        response = httpx.get(url=url, **kwargs)

    status = response.status_code
    if json:
        return Response(resobj=response, data=response.json())
    else:
        return Response(resobj=response, data=response.text)


def post(url: str, data: dict, session: Optional[Web] = None) -> Response:
    if session is not None:
        session.client.post(url=url, data=data, timeout=session.timeout)
    else:
        response = httpx.post(url=url, data=data)
    return Response(response, response.text)
