from __future__ import annotations

from typing import Any, List

from lib.integrations.catalog.models import (
    CatalogDto,
    CatalogStatusEnum,
    CatalogTypeEnum,
    CatalogVisibilityEnum,
    MediaTypeEnum,
)


def parse_catalog_item(data: dict[str, Any]) -> CatalogDto:
    return CatalogDto(
        id=data["id"],
        title=data["title"],
        description=data["description"],
        type=CatalogTypeEnum(data["type"]),
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
