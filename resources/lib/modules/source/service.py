from __future__ import annotations

import time
from typing import Optional

import xbmc
import xbmcgui

from lib.common import ADDON, log
from lib.integrations.source import source_api
from lib.integrations.source.models import (
    KodiIntegrationStreamsParametersQuery,
    PairStatusRequestDto,
    Status,
)


def decode_route_label(value: Optional[str]) -> Optional[str]:
    if not value:
        return None
    value = str(value).strip()
    return value or None


def get_stream_information(
    imdb_id: str,
    series: Optional[KodiIntegrationStreamsParametersQuery] = None,
):
    try:
        response = source_api.get_streams(
            imdb_id=imdb_id,
            series=series,
        )

        return response
    except Exception as error:
        error_message = str(error)

        log(error_message, xbmc.LOGERROR)

        raise error


def setup_source():
    dialog = xbmcgui.Dialog()
    addon_name = ADDON.getAddonInfo("name")

    dialog.ok(
        heading="Bejelentkezés a StremHU Source-ba",
        message="A bejelentkezéshez szükséged lesz a StremHU Source URL címére.\n\n"
        "Ezt megtalálod a StremHU Source felületén, a 'Támogatott kliensek' szekciónál.\n\n"
        "A folytatásban meg kell adnod ezt a címet!",
    )

    while True:
        current_url = ADDON.getSetting("source_url")
        source_url = dialog.input(
            heading="Add meg a StremHU Source URL-t",
            defaultt=current_url,
            type=xbmcgui.INPUT_ALPHANUM,
        ).strip()

        if not source_url:
            ADDON.openSettings()
            return

        source_url = source_url.rstrip("/")
        ADDON.setSetting("source_url", source_url)

        progress = xbmcgui.DialogProgress()
        progress.create(
            heading=addon_name,
            message="Kapcsolat ellenőrzése...",
        )

        try:
            source_api.get_health()
            break
        except Exception:
            progress.close()
            dialog.ok(
                heading=f"{addon_name} - Hiba",
                message="A megadott URL-en nem érhető el StremHU Source szolgáltatás!\n\n"
                "Kérlek ellenőrizd az URL-t és próbáld újra.",
            )

    try:
        pair_init = source_api.init_pair()
        progress.create(
            heading=f"{pair_init.userCode} - StremHU Source aktiváló kód",
            message=f"Látogass el a [B]{source_url}/activate[/B] felületére és add meg a kódot: [B]{pair_init.userCode}[/B]",
        )
    except Exception:
        xbmcgui.Dialog().notification(
            heading=addon_name,
            message="Nem sikerült elindítani a bejelentkezést, próbáld újra",
            icon=xbmcgui.NOTIFICATION_ERROR,
        )
        ADDON.openSettings()
        return

    success = False
    token = None

    while not progress.iscanceled():
        progress.update(
            percent=-1,
        )

        try:
            status_request = PairStatusRequestDto(
                deviceCode=pair_init.deviceCode,
            )
            status_response = source_api.get_pair_status(
                data=status_request,
            )

            if status_response.status == Status.linked:
                success = True
                token = status_response.token
                break

            if status_response.status == Status.expired:
                xbmcgui.Dialog().notification(
                    heading=addon_name,
                    message="A összekapcsolási kód lejárt, próbáld újra",
                    icon=xbmcgui.NOTIFICATION_ERROR,
                )
                break

        except Exception as e:
            log(f"Pairing poll error: {str(e)}", xbmc.LOGWARNING)

        time.sleep(1)

    progress.close()

    if success and token:
        ADDON.setSetting("source_token", token)
        xbmcgui.Dialog().notification(
            heading=addon_name,
            message="Sikeres bejelentkezés a StremHU Source-ba",
            icon=xbmcgui.NOTIFICATION_INFO,
        )
    elif not success:
        xbmcgui.Dialog().notification(
            heading=addon_name,
            message="Hiba történt a bejelentkezés során, próbáld újra",
            icon=xbmcgui.NOTIFICATION_WARNING,
        )

    ADDON.openSettings()


def logout_source():
    ADDON.setSetting("source_url", "")
    ADDON.setSetting("source_token", "")

    xbmcgui.Dialog().notification(
        heading=ADDON.getAddonInfo("name"),
        message="Sikeres kijelentkezés a StremHU Source-ból",
        icon=xbmcgui.NOTIFICATION_INFO,
    )

    ADDON.openSettings()
