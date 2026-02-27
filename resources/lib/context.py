import routing
import xbmcaddon

ADDON = xbmcaddon.Addon()
ADDON_ID = ADDON.getAddonInfo("id")
PLUGIN = routing.Plugin()

PLAYER_RULE_FILENAME = "stremhu.json"
TMDB_HELPER_ID = "plugin.video.themoviedb.helper"
