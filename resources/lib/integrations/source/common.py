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

    url = f"{base_url}/api/{normalized_path}"

    return plugin_request(
        method=method,
        url=url,
        params=params,
        data=data,
    )


def get_path_with_source_token(path: str) -> str:
    token = get_setting("source_token")
    if not token:
        raise ValueError("Source token not set")

    normalized_path = path.lstrip("/")
    return f"/{token}/{normalized_path}"
