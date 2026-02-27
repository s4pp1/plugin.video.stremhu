from typing import Any

from .models.stremhu_source_models import (
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
        requiresFullDownload=bool(data["requiresFullDownload"]),
        url=data["url"],
        detailsPath=data["detailsPath"],
    )


def parse_stream_item(data: dict[str, Any]) -> KodiImdbStreamDto:
    languages = [parse_language_meta(raw) for raw in data["languages"]]
    video_qualities = [parse_video_quality_meta(raw) for raw in data["videoQualities"]]
    file_size_value = data.get("fileSize") or data.get("size") or ""

    audio_quality_raw = data.get("audioQuality")
    audio_spatial_raw = data.get("audioSpatial")

    return KodiImdbStreamDto(
        torrentName=data["torrentName"],
        fileName=data["fileName"],
        seeders=data["seeders"],
        size=str(file_size_value),
        tracker=parse_tracker_meta(data["tracker"]),
        languages=languages,
        resolution=parse_resolution_meta(data["resolution"]),
        videoQualities=video_qualities,
        source=parse_source_meta(data["source"]),
        url=data["url"],
        audioQuality=parse_audio_quality_meta(audio_quality_raw)
        if audio_quality_raw is not None
        else None,
        audioSpatial=parse_audio_spatial_meta(audio_spatial_raw)
        if audio_spatial_raw is not None
        else None,
    )


def parse_streams_response(data: Any) -> KodiImdbStreamsDto:
    if isinstance(data, list):
        streams_raw = data
        errors_raw: list[Any] = []
    else:
        payload = data if isinstance(data, dict) else {}
        streams_raw = (
            payload.get("streams")
            or payload.get("items")
            or payload.get("results")
            or payload.get("data")
            or []
        )
        errors_raw = payload.get("errors") or []

    return KodiImdbStreamsDto(
        streams=[parse_stream_item(raw) for raw in streams_raw],
        errors=[str(item) for item in errors_raw],
    )
