from __future__ import annotations

from typing import Any

from lib.integrations.source.models import (
    AttributeResponse,
    IndexerDefinitionResponse,
    KodiImdbStreamResponse,
    KodiImdbStreamsResponse,
    PairInitResponse,
    PairStatusResponse,
    SuccessResponse,
)


def parse_health_response(data: Any) -> SuccessResponse:
    if not isinstance(data, dict):
        raise TypeError("Health response must be an object")

    return SuccessResponse(
        success=data["success"],
        message=data.get("message"),
    )


def parse_indexer_definition(data: dict[str, Any]) -> IndexerDefinitionResponse:
    return IndexerDefinitionResponse(
        id=data["id"],
        name=data["name"],
        url=data["url"],
        details_path=data["detailsPath"],
        requires_full_download=data["requiresFullDownload"],
    )


def parse_attribute_response(data: dict[str, Any]) -> AttributeResponse:
    return AttributeResponse(
        id=data["id"],
        name=data["name"],
        short_name=data.get("shortName"),
        preference_id=data.get("preferenceId"),
    )


def parse_stream_item(data: dict[str, Any]) -> KodiImdbStreamResponse:
    return KodiImdbStreamResponse(
        torrent_name=data["torrentName"],
        file_name=data["fileName"],
        seeders=data["seeders"],
        size=data["size"],
        indexer=parse_indexer_definition(data["indexer"]),
        media_attributes=[
            parse_attribute_response(attr) for attr in data["mediaAttributes"]
        ],
        url=data["url"],
    )


def parse_streams_response(data: Any) -> KodiImdbStreamsResponse:
    if not isinstance(data, dict):
        raise TypeError("Streams response must be an object")

    return KodiImdbStreamsResponse(
        streams=[parse_stream_item(raw) for raw in data["streams"]],
        errors=data["errors"],
    )


def parse_pair_init_response(data: Any) -> PairInitResponse:
    if not isinstance(data, dict):
        raise TypeError("Pair init response must be an object")

    return PairInitResponse(
        user_code=data["userCode"],
        device_code=data["deviceCode"],
        expires_at=data["expiresAt"],
    )


def parse_pair_status_response(data: Any) -> PairStatusResponse:
    if not isinstance(data, dict):
        raise TypeError("Pair status response must be an object")

    return PairStatusResponse(
        status=data["status"],
        token=data.get("token", None),
    )
