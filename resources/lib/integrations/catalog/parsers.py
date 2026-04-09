from __future__ import annotations

from typing import Any, List

from lib.integrations.catalog.models import (
    PublicCatalogDto,
    MediaTypeEnum,
)


def parse_catalog_item(data: dict[str, Any]) -> PublicCatalogDto:
    return PublicCatalogDto(
        id=data["id"],
        title=data["title"],
        description=data["description"],
        mediaType=MediaTypeEnum(data["mediaType"]),
        createdAt=data["createdAt"],
        updatedAt=data["updatedAt"],
    )


def parse_catalogs_response(data: Any) -> List[PublicCatalogDto]:
    if not isinstance(data, list):
        raise TypeError("Catalog response must be a list")

    return [parse_catalog_item(item) for item in data]
