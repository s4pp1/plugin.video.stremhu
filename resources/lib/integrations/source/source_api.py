from __future__ import annotations

from dataclasses import asdict
from typing import Optional

from lib.integrations.source.common import source_request
from lib.integrations.source.models import (
    KodiImdbStreamsDto,
    StreamsParametersQuery,
)
from lib.integrations.source.parsers import parse_streams_response


def get_streams(
    imdb_id: str,
    series: Optional[StreamsParametersQuery] = None,
) -> KodiImdbStreamsDto:

    path = f"/imdb/{imdb_id}/streams"

    series_dict = series and asdict(series)

    data = source_request(
        method="GET",
        path=path,
        params=series_dict,
    )

    payload = parse_streams_response(data)

    return payload
