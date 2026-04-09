from __future__ import annotations

from typing import List

from lib.integrations.catalog.common import catalog_request
from lib.integrations.catalog.models import PublicCatalogDto
from lib.integrations.catalog.parsers import parse_catalogs_response


def get_catalogs() -> List[PublicCatalogDto]:
    path = "/catalogs"

    data = catalog_request(
        method="GET",
        path=path,
    )

    parsed_data = parse_catalogs_response(data)

    return parsed_data
