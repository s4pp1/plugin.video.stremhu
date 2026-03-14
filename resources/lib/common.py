from typing import Optional

import xbmc
import xbmcgui
import xbmcplugin

from .context import ADDON, ADDON_ID, PLUGIN


def log(
    msg: str,
    level=xbmc.LOGINFO,
):
    message = f"[{ADDON_ID}] {msg}"

    xbmc.log(
        msg=message,
        level=level,
    )


def notification(
    message: str,
    error: bool = False,
):
    icon = xbmcgui.NOTIFICATION_INFO
    if error:
        icon = xbmcgui.NOTIFICATION_ERROR

    xbmcgui.Dialog().notification(
        ADDON.getAddonInfo("name"),
        message,
        icon,
    )


def get_setting(key):
    return ADDON.getSetting(key).strip()


def end_directory_if_needed():
    if PLUGIN.handle >= 0:
        xbmcplugin.endOfDirectory(PLUGIN.handle)


def parse_int(value):
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def get_query_arg(name: str) -> Optional[str]:
    values = getattr(PLUGIN, "args", {}).get(name) or []
    if not values:
        return None
    value = values[0]
    if value is None:
        return None
    value = str(value).strip()
    return value or None


def ensure_settings():
    missing = []
    source_url = get_setting("source_url")
    catalog_token = get_setting("catalog_token")

    if not source_url:
        missing.append("URL")

    if not catalog_token:
        missing.append("Token")

    if missing:
        message = "Hiányzó kötelező beállítás: {}".format(", ".join(missing))
        notification(message, error=True)
        return False

    return True
