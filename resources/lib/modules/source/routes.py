from __future__ import annotations

from typing import Optional

import xbmcgui
import xbmcplugin

from lib.common import ensure_source_settings, get_query_arg, notification, parse_int
from lib.context import PLUGIN
from lib.integrations.source.models import KodiIntegrationStreamsParametersQuery
from lib.modules.source.presenter import choose_stream_and_play
from lib.modules.source.service import get_stream_information


@PLUGIN.route("/source/imdb/<imdb_id>")
def play_imdb(imdb_id: Optional[str]):

    title = get_query_arg("title")
    season = get_query_arg("season")
    episode = get_query_arg("episode")

    if not ensure_source_settings() or not imdb_id or not title:
        xbmcplugin.setResolvedUrl(
            PLUGIN.handle,
            False,
            xbmcgui.ListItem(),
        )
        return

    series: Optional[KodiIntegrationStreamsParametersQuery] = None

    season_number = parse_int(season)
    episode_number = parse_int(episode)

    if season_number is not None or episode_number is not None:
        series = KodiIntegrationStreamsParametersQuery(
            season=season_number,
            episode=episode_number,
        )

    try:
        stream_information = get_stream_information(
            imdb_id=imdb_id,
            series=series,
        )

        choose_stream_and_play(
            title=title,
            stream_information=stream_information,
        )
    except Exception as error:
        notification(
            str(error),
            error=True,
        )

        xbmcplugin.setResolvedUrl(
            handle=PLUGIN.handle,
            succeeded=False,
            listitem=xbmcgui.ListItem(),
        )


@PLUGIN.route("/source/setup")
def setup_source():
    from .service import setup_source

    setup_source()


@PLUGIN.route("/source/logout")
def logout_source():
    from .service import logout_source

    logout_source()
