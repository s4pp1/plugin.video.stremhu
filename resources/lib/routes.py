import xbmcgui
import xbmcplugin

from .common import (
    end_directory_if_needed,
    ensure_settings,
    loc,
    notification,
    parse_int,
)
from .context import ADDON, PLUGIN
from .player_rule import install_tmdb_helper_player_rule
from .ui import choose_stream_and_play


def decode_route_label(value: str | None) -> str | None:
    if not value:
        return None
    value = str(value).strip()
    return value or None


def get_query_arg(name: str) -> str | None:
    values = getattr(PLUGIN, "args", {}).get(name) or []
    if not values:
        return None
    value = values[0]
    if value is None:
        return None
    value = str(value).strip()
    return value or None


@PLUGIN.route("/")
def root():
    install_tmdb_helper_player_rule()
    if not ensure_settings():
        ADDON.openSettings()
    notification(loc(30060))
    end_directory_if_needed()


@PLUGIN.route("/settings/player/install/<plugin_id>")
def install_player(plugin_id: str | None):
    install_tmdb_helper_player_rule(
        plugin_id=plugin_id,
    )
    end_directory_if_needed()


@PLUGIN.route("/source/imdb/<imdb>")
def play_imdb(imdb: str | None):
    if not ensure_settings() or not imdb:
        xbmcplugin.setResolvedUrl(
            PLUGIN.handle,
            False,
            xbmcgui.ListItem(),
        )
        return

    title = get_query_arg("title")
    season = get_query_arg("season")
    episode = get_query_arg("episode")

    media_title = decode_route_label(title) or imdb
    season_number = parse_int(season)
    episode_number = parse_int(episode)

    is_series = season_number is not None or episode_number is not None

    if is_series:
        if season_number is None or episode_number is None:
            xbmcplugin.setResolvedUrl(
                PLUGIN.handle,
                False,
                xbmcgui.ListItem(),
            )
            return

        content_id = "{}:{}:{}".format(imdb, season_number, episode_number)

        choose_stream_and_play(
            media_type="series",
            content_id=content_id,
            title=media_title,
        )
        return

    choose_stream_and_play(
        media_type="movie",
        content_id=imdb,
        title=media_title,
    )


def run():
    PLUGIN.run()
