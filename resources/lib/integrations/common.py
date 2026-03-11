from __future__ import annotations

from typing import Optional

from lib.common import log
from requests import HTTPError, RequestException, request

from .errors import ApiError

DEFAULT_USER_AGENT = "Kodi-StremHU"


def plugin_request(
    method: str,
    url: str,
    params: Optional[dict] = None,
    data: Optional[dict] = None,
):
    headers = {
        "Accept": "application/json",
        "User-Agent": DEFAULT_USER_AGENT,
    }

    try:
        response = request(
            method=method,
            url=url,
            params=params,
            data=data,
            headers=headers,
            timeout=30,
        )

        response.raise_for_status()

        return response.json()
    except HTTPError as exception:
        message = "Váratlan hiba történt, kérlek jelezd a hibát a fejlesztőnek!"

        status_code = exception.response.status_code

        if status_code == 401:
            message = "Nincs jogosultságod a művelethez"

        if status_code == 404:
            message = "A kérést nem lehet teljesíteni!"

        if status_code == 400:
            message = str(exception)

        log(message)

        raise ApiError(message)
    except RequestException as exception:
        raise ApiError("Network error: {}".format(exception))
    except ValueError:
        raise ApiError("Invalid JSON response")
