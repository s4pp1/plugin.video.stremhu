from __future__ import annotations

from typing import Any

from lib.common import log
from lib.integrations.source.models import (
    AudioQualityEnum,
    AudioQualityMetaDto,
    AudioSpatialEnum,
    AudioSpatialMetaDto,
    HealthDto,
    KodiImdbStreamDto,
    KodiImdbStreamsDto,
    LanguageEnum,
    LanguageMetaDto,
    PairInitDto,
    PairStatusDto,
    ResolutionEnum,
    ResolutionMetaDto,
    SourceEnum,
    SourceMetaDto,
    Status,
    TrackerEnum,
    TrackerMetaDto,
    VideoQualityEnum,
    VideoQualityMetaDto,
)


def parse_health_response(data: Any) -> HealthDto:
    if not isinstance(data, dict):
        raise TypeError("Health response must be an object")

    return HealthDto(
        version=data["version"],
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


def parse_pair_init_response(data: Any) -> PairInitDto:
    if not isinstance(data, dict):
        raise TypeError("Pair init response must be an object")

    return PairInitDto(
        userCode=data["userCode"],
        deviceCode=data["deviceCode"],
        expiresAt=data["expiresAt"],
    )


def parse_pair_status_response(data: Any) -> PairStatusDto:
    if not isinstance(data, dict):
        raise TypeError("Pair status response must be an object")

    return PairStatusDto(
        status=Status(data["status"]),
        token=data.get("token", None),
    )
