from typing import Optional

from lib.common import get_setting
from lib.context import STREMHU_CATALOG_URL
from lib.integrations.common import plugin_request


def catalog_request(
    method: str,
    path: str,
    params: Optional[dict] = None,
    data: Optional[dict] = None,
):
    catalog_token = get_setting("catalog_token")

    base_url = f"{STREMHU_CATALOG_URL}/api/{catalog_token}/kodi"
    normalized_path = path.lstrip("/")

    url = f"{base_url}/{normalized_path}"

    return plugin_request(
        method=method,
        url=url,
        params=params,
        data=data,
    )
