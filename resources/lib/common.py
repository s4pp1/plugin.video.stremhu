import xbmc
import xbmcgui
import xbmcplugin

from .context import ADDON, ADDON_ID, PLUGIN


def loc(string_id: int):
    return ADDON.getLocalizedString(string_id)


def log(
    msg: str,
    level=xbmc.LOGINFO,
):
    message = "[{}] {}".format(ADDON_ID, msg)

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


def resolve_timeout_seconds():
    return 15


def ensure_settings():
    missing = []
    source_url = get_setting("source_url")

    if not source_url:
        missing.append(loc(30013))

    if missing:
        message = "{}: {}".format(loc(30040), ", ".join(missing))
        notification(message, error=True)
        return False

    return True


def normalize_media_type(media_type):
    if media_type == "movie":
        return "movie"
    if media_type in ("series", "episode"):
        return "series"
    return None
