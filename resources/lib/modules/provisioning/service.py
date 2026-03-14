import json
from typing import List

import xbmc
import xbmcgui
import xbmcvfs

from lib.common import log, notification
from lib.context import ADDON, TMDB_BINGIE_HELPER_ID, TMDB_HELPER_ID
from lib.modules.provisioning.constants import (
    ARTIFACT_INSTALL_PLAN,
    PROVISIONING_STATE_FILE,
)
from lib.modules.provisioning.schemas import ProvisioningItem, ProvisioningState


def ensure_on_startup():
    installed_helpers = _ensure_installed_helpers()

    if not installed_helpers:
        return

    for provisioning_item in ARTIFACT_INSTALL_PLAN:
        if provisioning_item.addon_id in installed_helpers:
            install_artifact(
                provisioning_item=provisioning_item,
            )


def install_artifact(
    provisioning_item: ProvisioningItem,
    force=False,
):
    has_addon = xbmc.getCondVisibility(f"System.HasAddon({provisioning_item.addon_id})")

    if not has_addon:
        notification(
            message=f'A(z) "{provisioning_item.addon_id}" addon nincs telepítve!',
            error=True,
        )
        return

    if not xbmcvfs.exists(provisioning_item.target_dir):
        xbmcvfs.mkdirs(provisioning_item.target_dir)

    addon_path = ADDON.getAddonInfo("path")
    source_path = (
        f"{addon_path}/resources/artifacts/{provisioning_item.artifact_filename}"
    )
    target_path = (
        f"{provisioning_item.target_dir}/{provisioning_item.artifact_filename}"
    )

    installed_version = _get_installed_version(provisioning_item)

    if xbmcvfs.exists(target_path) and not force:
        if installed_version >= provisioning_item.version:
            return True

    if xbmcvfs.exists(target_path) and force:
        xbmcvfs.delete(target_path)

    if not xbmcvfs.copy(source_path, target_path):
        log("Failed to copy player rule to {}".format(target_path), xbmc.LOGERROR)

        notification(
            message="Hiba történt a kiegészítő telepítésekor!",
            error=True,
        )

        return False

    _set_installed_version(provisioning_item)

    notification(
        message="A StremHU addon kiegészítő telepítve!",
    )


def _ensure_installed_helpers() -> List[str]:
    installed_helpers: List[str] = []

    has_tmdb_helper = xbmc.getCondVisibility(f"System.HasAddon({TMDB_HELPER_ID})")
    if has_tmdb_helper:
        installed_helpers.append(TMDB_HELPER_ID)

    has_tmdb_bingie_helper = xbmc.getCondVisibility(
        f"System.HasAddon({TMDB_BINGIE_HELPER_ID})"
    )
    if has_tmdb_bingie_helper:
        installed_helpers.append(TMDB_BINGIE_HELPER_ID)

    if installed_helpers:
        return installed_helpers

    xbmcgui.Dialog().ok(
        heading=ADDON.getAddonInfo("name"),
        message="A StremHU működéséhez legalább egy helper addon szükséges:\n"
        "- TMDb Helper vagy\n"
        "- TMDb Bingie Helper",
    )

    return installed_helpers


def _get_provisioning_state() -> ProvisioningState:
    if not xbmcvfs.exists(PROVISIONING_STATE_FILE):
        return ProvisioningState()

    try:
        with xbmcvfs.File(PROVISIONING_STATE_FILE) as f:
            data = json.loads(f.read())
            return ProvisioningState.from_dict(data)
    except Exception:
        return ProvisioningState()


def _save_provisioning_state(state: ProvisioningState):
    try:
        with xbmcvfs.File(PROVISIONING_STATE_FILE, "w") as f:
            f.write(json.dumps(state.to_dict(), indent=4))
    except Exception as e:
        log(f"Failed to save provisioning state: {e}", xbmc.LOGERROR)


def _get_installed_version(provisioning_item: ProvisioningItem) -> int:
    state = _get_provisioning_state()
    return state.get_version(
        addon_id=provisioning_item.addon_id,
        artifact_filename=provisioning_item.artifact_filename,
    )


def _set_installed_version(provisioning_item: ProvisioningItem):
    state = _get_provisioning_state()
    state.set_version(
        addon_id=provisioning_item.addon_id,
        artifact_filename=provisioning_item.artifact_filename,
        version=provisioning_item.version,
    )
    _save_provisioning_state(state)
