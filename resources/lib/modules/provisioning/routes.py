from __future__ import annotations

import lib.modules.provisioning.service as provisioning_service
from lib.common import end_directory_if_needed
from lib.context import PLUGIN
from lib.modules.provisioning.constants import ARTIFACT_INSTALL_PLAN


@PLUGIN.route("/provisioning/artifact/<addon_id>/install")
def install_artifact(addon_id: str):

    for provisioning_item in ARTIFACT_INSTALL_PLAN:
        if provisioning_item.addon_id == addon_id:
            provisioning_service.install_artifact(
                provisioning_item=provisioning_item,
                force=True,
            )

    end_directory_if_needed()
