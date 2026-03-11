from __future__ import annotations

from lib.common import end_directory_if_needed, ensure_settings, get_query_arg
from lib.context import ADDON, PLUGIN
from lib.modules.catalogs.presenter import render_widget_catalogs
from lib.modules.catalogs.service import get_catalogs


@PLUGIN.route("/widget/catalogs")
def widget_catalogs():
    addon_id = get_query_arg("addon_id")
    if not addon_id:
        end_directory_if_needed()
        return

    if not ensure_settings():
        ADDON.openSettings()
        end_directory_if_needed()
        return

    catalogs = get_catalogs()

    render_widget_catalogs(
        catalogs=catalogs,
        addon_id=addon_id,
    )
    end_directory_if_needed()
