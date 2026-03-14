from typing import List

from lib.modules.provisioning.schemas import ProvisioningItem

PROVISIONING_STATE_FILE = (
    "special://profile/addon_data/plugin.video.stremhu/provisioning_state.json"
)

TMDB_HELPER_ID = "plugin.video.themoviedb.helper"
TMDB_BINGIE_HELPER_ID = "plugin.video.tmdb.bingie.helper"

TMDB_HELPER_PLAYER_FILENAME = "stremhu-tmdb-hepler-player.json"
TMDB_HELPER_NODE_FILENAME = "stremhu-tmdb-hepler-node.json"

TMDB_BINGIE_HELPER_PLAYER_FILENAME = "stremhu-tmdb-bingie-hepler-player.json"
TMDB_BINGIE_HELPER_NODE_FILENAME = "stremhu-tmdb-bingie-hepler-node.json"


TMDB_HELPER_PLAYER = ProvisioningItem(
    version=1,
    addon_id=TMDB_HELPER_ID,
    artifact_filename=TMDB_HELPER_PLAYER_FILENAME,
    target_dir=f"special://profile/addon_data/{TMDB_HELPER_ID}/players",
)

TMDB_HELPER_NODE = ProvisioningItem(
    version=1,
    addon_id=TMDB_HELPER_ID,
    artifact_filename=TMDB_HELPER_NODE_FILENAME,
    target_dir=f"special://profile/addon_data/{TMDB_HELPER_ID}/nodes",
)

TMDB_BINGIE_HELPER_PLAYER = ProvisioningItem(
    version=1,
    addon_id=TMDB_BINGIE_HELPER_ID,
    artifact_filename=TMDB_BINGIE_HELPER_PLAYER_FILENAME,
    target_dir=f"special://profile/addon_data/{TMDB_BINGIE_HELPER_ID}/players",
)


TMDB_BINGIE_HELPER_NODE = ProvisioningItem(
    version=1,
    addon_id=TMDB_BINGIE_HELPER_ID,
    artifact_filename=TMDB_BINGIE_HELPER_NODE_FILENAME,
    target_dir=f"special://profile/addon_data/{TMDB_BINGIE_HELPER_ID}/nodes",
)

ARTIFACT_INSTALL_PLAN: List[ProvisioningItem] = [
    TMDB_HELPER_PLAYER,
    TMDB_HELPER_NODE,
    TMDB_BINGIE_HELPER_PLAYER,
    TMDB_BINGIE_HELPER_NODE,
]
