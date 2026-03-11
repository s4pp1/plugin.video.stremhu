from typing import Optional

from lib.common import get_setting
from lib.integrations.common import plugin_request


def source_request(
    method: str,
    path: str,
    params: Optional[dict] = None,
    data: Optional[dict] = None,
):
    base_url = get_setting("source_url").rstrip("/")
    normalized_path = path.lstrip("/")

    url = f"{base_url}/kodi/{normalized_path}"

    return plugin_request(
        method=method,
        url=url,
        params=params,
        data=data,
    )
