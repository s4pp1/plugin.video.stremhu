from __future__ import annotations

from typing import Any

from lib.common import log
from lib.integrations.source.models import (
    AudioQualityEnum,
    AudioQualityMetaDto,
    AudioSpatialEnum,
    AudioSpatialMetaDto,
    KodiImdbStreamDto,
    KodiImdbStreamsDto,
    LanguageEnum,
    LanguageMetaDto,
    ResolutionEnum,
    ResolutionMetaDto,
    SourceEnum,
    SourceMetaDto,
    TrackerEnum,
    TrackerMetaDto,
    VideoQualityEnum,
    VideoQualityMetaDto,
)


def parse_language_meta(data: dict[str, Any]) -> LanguageMetaDto:
    return LanguageMetaDto(
        value=LanguageEnum(data["value"]),
        label=data["label"],
    )


def parse_resolution_meta(data: dict[str, Any]) -> ResolutionMetaDto:
    return ResolutionMetaDto(
        value=ResolutionEnum(data["value"]),
        label=data["label"],
    )


def parse_video_quality_meta(data: dict[str, Any]) -> VideoQualityMetaDto:
    return VideoQualityMetaDto(
        value=VideoQualityEnum(data["value"]),
        label=data["label"],
    )


def parse_audio_quality_meta(data: dict[str, Any]) -> AudioQualityMetaDto:
    return AudioQualityMetaDto(
        value=AudioQualityEnum(data["value"]),
        label=data["label"],
    )


def parse_audio_spatial_meta(data: dict[str, Any]) -> AudioSpatialMetaDto:
    return AudioSpatialMetaDto(
        value=AudioSpatialEnum(data["value"]),
        label=data["label"],
    )


def parse_source_meta(data: dict[str, Any]) -> SourceMetaDto:
    return SourceMetaDto(
        value=SourceEnum(data["value"]),
        label=data["label"],
    )


def parse_tracker_meta(data: dict[str, Any]) -> TrackerMetaDto:
    return TrackerMetaDto(
        value=TrackerEnum(data["value"]),
        label=data["label"],
        requiresFullDownload=data["requiresFullDownload"],
        url=data["url"],
        detailsPath=data["detailsPath"],
    )


def parse_stream_item(data: dict[str, Any]) -> KodiImdbStreamDto:
    log("{}".format(data))

    return KodiImdbStreamDto(
        torrentName=data["torrentName"],
        fileName=data["fileName"],
        seeders=data["seeders"],
        size=data["size"],
        tracker=parse_tracker_meta(data["tracker"]),
        languages=[parse_language_meta(raw) for raw in data["languages"]],
        resolution=parse_resolution_meta(data["resolution"]),
        videoQualities=[
            parse_video_quality_meta(raw) for raw in data["videoQualities"]
        ],
        source=parse_source_meta(data["source"]),
        url=data["url"],
        audioQuality=parse_audio_quality_meta(data["audioQuality"])
        if data.get("audioQuality") is not None
        else None,
        audioSpatial=parse_audio_spatial_meta(data["audioSpatial"])
        if data.get("audioSpatial") is not None
        else None,
    )


def parse_streams_response(data: Any) -> KodiImdbStreamsDto:
    if not isinstance(data, dict):
        raise TypeError("Streams response must be an object")

    return KodiImdbStreamsDto(
        streams=[parse_stream_item(raw) for raw in data["streams"]],
        errors=data["errors"],
    )
