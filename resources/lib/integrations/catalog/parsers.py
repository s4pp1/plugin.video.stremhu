from __future__ import annotations

from typing import Any, List

from lib.integrations.catalog.models import (
    CatalogAutoRulesDto,
    CatalogDto,
    CatalogStatusEnum,
    CatalogTypeEnum,
    CatalogVisibilityEnum,
    MediaTypeEnum,
)


def parse_catalog_auto_rules(data: dict[str, Any]) -> CatalogAutoRulesDto:
    streaming_providers_raw = data.get("streamingProviders")
    genres_raw = data.get("genres")

    return CatalogAutoRulesDto(
        itemsCount=int(data["itemsCount"]),
        streamingProviders=[int(value) for value in streaming_providers_raw]
        if streaming_providers_raw is not None
        else None,
        genres=[int(value) for value in genres_raw] if genres_raw is not None else None,
    )


def parse_catalog_item(data: dict[str, Any]) -> CatalogDto:
    return CatalogDto(
        id=data["id"],
        title=data["title"],
        description=data["description"],
        type=CatalogTypeEnum(data["type"]),
        autoRules=parse_catalog_auto_rules(data["autoRules"]),
        visibility=CatalogVisibilityEnum(data["visibility"]),
        status=CatalogStatusEnum(data["status"]),
        mediaType=MediaTypeEnum(data["mediaType"]),
        isOfficial=bool(data["isOfficial"]),
        createdAt=data["createdAt"],
        updatedAt=data["updatedAt"],
    )


def parse_catalogs_response(data: Any) -> List[CatalogDto]:
    if not isinstance(data, list):
        raise TypeError("Catalog response must be a list")

    return [parse_catalog_item(item) for item in data]
