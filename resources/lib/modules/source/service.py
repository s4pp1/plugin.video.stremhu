from __future__ import annotations

from typing import Optional

import xbmc

from lib.common import log
from lib.integrations.source import source_api
from lib.integrations.source.models import StreamsParametersQuery


def decode_route_label(value: Optional[str]) -> Optional[str]:
    if not value:
        return None
    value = str(value).strip()
    return value or None


def get_stream_information(
    imdb_id: str,
    series: Optional[StreamsParametersQuery] = None,
):
    try:
        response = source_api.get_streams(
            imdb_id=imdb_id,
            series=series,
        )

        return response
    except Exception as error:
        error_message = str(error)

        log(error_message, xbmc.LOGERROR)

        raise error
