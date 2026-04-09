from __future__ import annotations

import xbmc
import xbmcgui
import xbmcplugin

from lib.context import ADDON, PLUGIN
from lib.modules.provisioning.routes import install_artifact


def render_main_menu():
    if PLUGIN.handle < 0:
        return

    addon_icon = ADDON.getAddonInfo("icon")

    info_item = xbmcgui.ListItem(
        label="StremHU - Információ",
    )
    info_item.setArt({"icon": addon_icon, "thumb": addon_icon})
    info_item.setProperty("IsPlayable", "false")

    xbmcplugin.addDirectoryItem(
        handle=PLUGIN.handle,
        url=PLUGIN.url_for_path("/main/info"),
        listitem=info_item,
        isFolder=False,
    )

    settings_item = xbmcgui.ListItem(
        label="Beállítások",
    )
    settings_item.setArt(
        {
            "icon": "DefaultAddonSettings.png",
            "thumb": "DefaultAddonSettings.png",
        }
    )
    settings_item.setProperty("IsPlayable", "false")

    xbmcplugin.addDirectoryItem(
        handle=PLUGIN.handle,
        url=PLUGIN.url_for_path("/main/settings"),
        listitem=settings_item,
        isFolder=False,
    )

    if xbmc.getCondVisibility("System.HasAddon(plugin.video.themoviedb.helper)"):
        tmdb_item = xbmcgui.ListItem(
            label="TMDb Helper beállítása",
        )
        tmdb_item.setArt(
            {
                "icon": addon_icon,
                "thumb": addon_icon,
            }
        )
        tmdb_item.setProperty("IsPlayable", "false")

        setup_url = PLUGIN.url_for(
            install_artifact,
            addon_id="plugin.video.themoviedb.helper",
        )

        xbmcplugin.addDirectoryItem(
            handle=PLUGIN.handle,
            url=setup_url,
            listitem=tmdb_item,
            isFolder=False,
        )

    # 4. Bingie Helper Setup (if installed)
    if xbmc.getCondVisibility("System.HasAddon(plugin.video.tmdb.bingie.helper)"):
        bingie_item = xbmcgui.ListItem(
            label="Bingie Helper beállítása",
        )
        bingie_item.setArt(
            {
                "icon": addon_icon,
                "thumb": addon_icon,
            }
        )
        bingie_item.setProperty("IsPlayable", "false")

        setup_url = PLUGIN.url_for(
            install_artifact,
            addon_id="plugin.video.tmdb.bingie.helper",
        )

        xbmcplugin.addDirectoryItem(
            handle=PLUGIN.handle,
            url=setup_url,
            listitem=bingie_item,
            isFolder=False,
        )

    xbmcplugin.endOfDirectory(PLUGIN.handle)


def root_info():
    dialog = xbmcgui.Dialog()
    message = (
        "A StremHU addon egy háttérszolgáltatás, amely közvetlen elérést biztosít "
        "magyar trackerekhez.\n\n"
        "A legjobb élmény érdekében használd a [B]TMDb Helper[/B] vagy [B]Bingie Helper[/B] "
        "kiegészítőket, amelyekben kiválaszthatod a StremHU-t lejátszónak."
    )
    dialog.ok(
        "StremHU",
        message,
    )


def open_settings():
    ADDON.openSettings()
