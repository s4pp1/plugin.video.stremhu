from typing import Any, List

import xbmc
import xbmcgui
import xbmcplugin
import xbmcvfs

from .api import fetch_streams
from .common import loc, log, notification
from .context import ADDON, PLUGIN
from .errors import ApiError
from .models.stremhu_source_models import KodiImdbStreamDto


def resolve_stream_icon(stream: KodiImdbStreamDto) -> str:
    resolution = stream.resolution.value.value
    icon_path = "{}/resources/media/{}.png".format(
        ADDON.getAddonInfo("path"),
        resolution,
    )
    if xbmcvfs.exists(icon_path):
        return icon_path
    return ADDON.getAddonInfo("icon")


def join_meta_labels(items: list[Any]) -> str:
    labels = [str(item.label).strip() for item in items if getattr(item, "label", "")]
    return ", ".join([label for label in labels if label])


def join_non_empty_parts(parts: list[str | None]) -> str:
    return ", ".join([part for part in parts if part])


def format_seeders(seeders: float) -> str:
    return f"{int(seeders)} seed"


def build_stream_label(stream: KodiImdbStreamDto) -> str:
    tracker_label = f"{stream.tracker.label}"
    video_qualities = join_meta_labels(stream.videoQualities)
    languages = join_meta_labels(stream.languages)

    return join_non_empty_parts([tracker_label, video_qualities, languages])


def build_stream_label2(stream: KodiImdbStreamDto) -> str:
    audio_quality = stream.audioQuality.label if stream.audioQuality else None
    audio_spatial = stream.audioSpatial.label if stream.audioSpatial else None

    return join_non_empty_parts(
        [
            audio_quality,
            audio_spatial,
            format_seeders(stream.seeders),
            stream.size,
        ]
    )


def choose_stream_and_play(
    media_type: str,
    content_id: str,
    title: str,
):
    try:
        streams = fetch_streams(
            media_type=media_type,
            content_id=content_id,
        )
    except ApiError as exc:
        log(str(exc), xbmc.LOGERROR)
        notification(str(exc), error=True)
        xbmcplugin.setResolvedUrl(
            PLUGIN.handle,
            False,
            xbmcgui.ListItem(),
        )
        return

    if not streams:
        xbmcgui.Dialog().ok(loc(30032), loc(30043))
        xbmcplugin.setResolvedUrl(
            PLUGIN.handle,
            False,
            xbmcgui.ListItem(),
        )
        return

    items: List[xbmcgui.ListItem] = []
    for stream in streams:
        icon = resolve_stream_icon(stream)
        li = xbmcgui.ListItem(
            label=build_stream_label(stream),
        )
        li.setLabel2(build_stream_label2(stream))
        li.setArt({"icon": icon, "thumb": icon})
        items.append(li)

    heading = loc(30032)
    selected_index = xbmcgui.Dialog().select(
        heading=heading,
        list=items,
        useDetails=True,
    )

    if selected_index < 0:
        xbmcplugin.setResolvedUrl(PLUGIN.handle, False, xbmcgui.ListItem())
        return

    selected_stream = streams[selected_index]
    play_item = xbmcgui.ListItem(path=selected_stream.url)
    play_item.setProperty("IsPlayable", "true")
    play_item.setInfo("video", {"title": title or selected_stream.torrentName})
    xbmcplugin.setResolvedUrl(PLUGIN.handle, True, play_item)
