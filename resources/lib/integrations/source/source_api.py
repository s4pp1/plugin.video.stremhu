from __future__ import annotations

from dataclasses import asdict
from typing import Optional

from lib.integrations.source.common import get_path_with_source_token, source_request
from lib.integrations.source.models import (
    HealthDto,
    KodiImdbStreamsDto,
    KodiIntegrationStreamsParametersQuery,
    PairInitDto,
    PairStatusDto,
    PairStatusRequestDto,
)
from lib.integrations.source.parsers import (
    parse_health_response,
    parse_pair_init_response,
    parse_pair_status_response,
    parse_streams_response,
)


def get_health() -> HealthDto:
    path = "/health"

    data = source_request(
        method="GET",
        path=path,
    )

    parsed = parse_health_response(data)
    return parsed


def get_streams(
    imdb_id: str,
    series: Optional[KodiIntegrationStreamsParametersQuery] = None,
) -> KodiImdbStreamsDto:

    path = get_path_with_source_token(f"/kodi/imdb/{imdb_id}/streams")

    series_dict = series and asdict(series)

    data = source_request(
        method="GET",
        path=path,
        params=series_dict,
    )

    parsed = parse_streams_response(data)
    return parsed


def init_pair() -> PairInitDto:
    path = "/auth/pair/init"

    data = source_request(
        method="POST",
        path=path,
    )

    parsed = parse_pair_init_response(data)
    return parsed


def get_pair_status(data: PairStatusRequestDto) -> PairStatusDto:
    path = "/auth/pair/status"

    data_dict = asdict(data)

    data = source_request(
        method="POST",
        path=path,
        data=data_dict,
    )

    parsed = parse_pair_status_response(data)
    return parsed
