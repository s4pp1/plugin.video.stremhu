from __future__ import annotations

from typing import List, Sequence

import xbmcgui
import xbmcplugin
import xbmcvfs

from ...common import notification
from ...context import ADDON, PLUGIN
from ...integrations.source.models import (
    KodiImdbStreamResponse,
    KodiImdbStreamsResponse,
)


def resolve_resolution_icon(
    stream: KodiImdbStreamResponse,
) -> str:
    resolutions = [
        attr.id
        for attr in stream.media_attributes
        if attr.preference_id == "resolution"
    ]
    if resolutions:
        resolution = resolutions[0]
        icon_path = "{}/resources/media/resolution/{}.png".format(
            ADDON.getAddonInfo("path"),
            resolution,
        )
        if xbmcvfs.exists(icon_path):
            return icon_path

    return ADDON.getAddonInfo("icon")


def join_non_empty_parts(parts: Sequence[str | None]) -> str:
    return ", ".join([part for part in parts if part])


def format_seeders(seeders: float) -> str:
    return f"{int(seeders)} seed"


def build_stream_label(stream: KodiImdbStreamResponse) -> str:
    indexer_name = f"{stream.indexer.name}"
    video_qualities = ", ".join(
        [
            attr.short_name or attr.name
            for attr in stream.media_attributes
            if attr.preference_id == "video-quality"
        ]
    )
    languages = ", ".join(
        [
            attr.short_name or attr.name
            for attr in stream.media_attributes
            if attr.preference_id == "language"
        ]
    )

    return join_non_empty_parts([indexer_name, video_qualities, languages])


def build_stream_label2(stream: KodiImdbStreamResponse) -> str:
    audio_qualities = ", ".join(
        [
            attr.short_name or attr.name
            for attr in stream.media_attributes
            if attr.preference_id == "audio-quality"
        ]
    )
    audio_spatials = ", ".join(
        [
            attr.short_name or attr.name
            for attr in stream.media_attributes
            if attr.preference_id == "audio-spatial"
        ]
    )

    return join_non_empty_parts(
        [
            audio_qualities,
            audio_spatials,
            format_seeders(stream.seeders),
            stream.size,
        ]
    )


def choose_stream_and_play(
    stream_information: KodiImdbStreamsResponse,
):

    if stream_information.errors:
        notification(
            message=" ,".join(stream_information.errors),
            error=True,
        )

    if not stream_information.streams:
        xbmcgui.Dialog().ok(
            heading="Nincs elérhető torrent",
            message="Ehhez a tartalomhoz nincs elérhető torrent, vagy nincs találat a StremHU Source beállításai alapján.",
        )
        xbmcplugin.setResolvedUrl(
            handle=PLUGIN.handle,
            succeeded=False,
            listitem=xbmcgui.ListItem(),
        )
        return

    items: List[str | xbmcgui.ListItem] = []

    for stream in stream_information.streams:
        icon = resolve_resolution_icon(stream)

        li = xbmcgui.ListItem(
            label=build_stream_label(stream),
            label2=build_stream_label2(stream),
        )
        li.setArt({"icon": icon, "thumb": icon})

        items.append(li)

    heading = "Stream kiválasztása"
    selected_index = xbmcgui.Dialog().select(
        heading=heading,
        list=items,
        useDetails=True,
    )

    if selected_index < 0:
        xbmcplugin.setResolvedUrl(
            handle=PLUGIN.handle,
            succeeded=False,
            listitem=xbmcgui.ListItem(),
        )
        return

    selected_stream = stream_information.streams[selected_index]
    play_item = xbmcgui.ListItem(path=selected_stream.url)
    play_item.setProperty("IsPlayable", "true")
    xbmcplugin.setResolvedUrl(
        handle=PLUGIN.handle,
        succeeded=True,
        listitem=play_item,
    )
