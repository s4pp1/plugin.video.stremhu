from __future__ import annotations

from typing import List

import xbmcgui
import xbmcplugin

from lib.common import get_setting
from lib.context import ADDON, PLUGIN, STREMHU_CATALOG_URL
from lib.integrations.catalog.models import CatalogDto, MediaTypeEnum


def render_widget_catalogs(
    catalogs: List[CatalogDto],
    addon_id: str,
):
    if PLUGIN.handle < 0:
        return

    catalog_token = get_setting("catalog_token")
    addon_icon = ADDON.getAddonInfo("icon")

    for catalog in catalogs:
        media = "Filmek"

        if catalog.mediaType == MediaTypeEnum.series:
            media = "Sorozatok"

        list_item = xbmcgui.ListItem(
            label=f"{catalog.title} - {media}",
        )
        list_item.setProperty("IsPlayable", "false")
        list_item.setArt(
            {
                "icon": addon_icon,
                "thumb": addon_icon,
            }
        )

        list_url = f"{STREMHU_CATALOG_URL}/api/{catalog_token}/kodi/catalogs/{catalog.id}/items"
        tmdb_url = f"plugin://{addon_id}/?info=mdblist_locallist&&{list_url}"

        xbmcplugin.addDirectoryItem(
            handle=PLUGIN.handle,
            url=tmdb_url,
            listitem=list_item,
            isFolder=True,
        )
