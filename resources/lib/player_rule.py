import xbmc
import xbmcvfs

from .common import loc, log, notification
from .context import ADDON, PLAYER_RULE_FILENAME, TMDB_HELPER_ID


def install_tmdb_helper_player_rule(
    force: bool = False,
    show_feedback: bool = False,
):
    if not xbmc.getCondVisibility("System.HasAddon({})".format(TMDB_HELPER_ID)):
        log(
            "TMDB Helper is not installed, player rule install skipped", xbmc.LOGWARNING
        )
        if show_feedback:
            notification(
                loc(30075),
                error=True,
            )
        return False

    addon_path = ADDON.getAddonInfo("path")
    source_path = "{}/resources/players/{}".format(addon_path, PLAYER_RULE_FILENAME)
    target_dir = "special://profile/addon_data/{}/players".format(TMDB_HELPER_ID)
    target_path = "{}/{}".format(target_dir, PLAYER_RULE_FILENAME)

    if not xbmcvfs.exists(source_path):
        log("Player rule template missing: {}".format(source_path), xbmc.LOGERROR)
        if show_feedback:
            notification(loc(30074), error=True)
        return False

    if not xbmcvfs.exists(target_dir):
        xbmcvfs.mkdirs(target_dir)

    if not force and xbmcvfs.exists(target_path):
        if show_feedback:
            notification(loc(30073))
        return True

    if force and xbmcvfs.exists(target_path):
        xbmcvfs.delete(target_path)

    if not xbmcvfs.copy(source_path, target_path):
        log("Failed to copy player rule to {}".format(target_path), xbmc.LOGERROR)
        if show_feedback:
            notification(loc(30074), error=True)
        return False

    if show_feedback:
        notification(loc(30072))

    return True
