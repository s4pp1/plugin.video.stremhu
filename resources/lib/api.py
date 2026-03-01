import urllib.parse

import requests

from .common import get_setting, resolve_timeout_seconds
from .errors import ApiError
from .models.stremhu_source_models import KodiImdbStreamsDto
from .parsers import parse_streams_response


def request_json(url: str):
    headers = {
        "Accept": "application/json",
        "User-Agent": "Kodi-StremHU-Source/0.1.0",
    }

    try:
        response = requests.get(
            url,
            headers=headers,
            timeout=resolve_timeout_seconds(),
        )
        response.raise_for_status()
        return response.json()
    except requests.HTTPError as exc:
        status_code = exc.response.status_code if exc.response is not None else "?"
        raise ApiError("HTTP {} - {}".format(status_code, url))
    except requests.RequestException as exc:
        raise ApiError("Network error: {}".format(exc))
    except ValueError:
        raise ApiError("Invalid JSON response")


def resolve_imdb_and_query(
    media_type: str,
    content_id: str,
) -> tuple[str, dict[str, str]]:
    if media_type not in ("series", "episode"):
        return content_id, {}

    parts = content_id.split(":")
    if len(parts) == 3 and parts[1].isdigit() and parts[2].isdigit():
        imdb_id = parts[0]
        return imdb_id, {"season": str(int(parts[1])), "episode": str(int(parts[2]))}

    return content_id, {}


def build_streams_url(media_type: str, content_id: str) -> str:
    source_url = get_setting("source_url").rstrip("/")
    imdb_id, query_params = resolve_imdb_and_query(
        media_type=media_type,
        content_id=content_id,
    )
    encoded_imdb_id = urllib.parse.quote(imdb_id, safe="")
    url = "{}/kodi/imdb/{}/streams".format(source_url, encoded_imdb_id)

    if query_params:
        return "{}?{}".format(url, urllib.parse.urlencode(query_params))
    return url


def fetch_streams(
    media_type: str,
    content_id: str,
) -> KodiImdbStreamsDto:
    url = build_streams_url(media_type=media_type, content_id=content_id)
    data = request_json(url)
    try:
        payload = parse_streams_response(data)
        return payload
    except (KeyError, TypeError, ValueError):
        raise ApiError("Invalid response format")
