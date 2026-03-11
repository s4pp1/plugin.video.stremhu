import routing
import xbmcaddon

ADDON = xbmcaddon.Addon()
ADDON_ID = ADDON.getAddonInfo("id")
PLUGIN = routing.Plugin()

TMDB_HELPER_ID = "plugin.video.themoviedb.helper"
TMDB_BINGIE_HELPER_ID = "plugin.video.tmdb.bingie.helper"

STREMHU_CATALOG_URL = "https://catalog.stremhu.app"
