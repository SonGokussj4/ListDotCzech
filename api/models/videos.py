from __future__ import annotations

from typing import Any, Optional

from pydantic import BaseModel, Field


class ExtraTextItem(BaseModel):
    uri: str
    language: str
    kind: str
    mime: str


class LicenseServers(BaseModel):
    com_widevine_alpha: str | None = Field(None, alias='com.widevine.alpha')
    org_w3_clearkey: str | None = Field(None, alias='org.w3.clearkey')
    com_microsoft_playready: str | None = Field(
        None, alias='com.microsoft.playready'
    )


class LicenseRequestHeaders(BaseModel):
    X_AxDRM_Message: str | None = Field(None, alias='X-AxDRM-Message')


class ComWidevineAlpha(BaseModel):
    serverCertificateUri: str


class Advanced(BaseModel):
    com_widevine_alpha: ComWidevineAlpha = Field(..., alias='com.widevine.alpha')


class Drm(BaseModel):
    advanced: Advanced


class ExtraConfigItem(BaseModel):
    drm: Drm


class Track(BaseModel):
    id: int
    active: bool
    type: str
    bandwidth: int
    language: str
    label: str | None
    kind: Any
    width: int
    height: int
    frameRate: int | None
    pixelAspectRatio: Any
    hdr: Any
    mimeType: str
    audioMimeType: str
    videoMimeType: str
    codecs: str
    audioCodec: str
    videoCodec: str
    primary: bool
    roles: list[Any]
    audioRoles: list[Any]
    forced: bool
    videoId: int
    audioId: int
    channelsCount: Any
    audioSamplingRate: Any
    spatialAudio: bool
    tilesLayout: Any
    audioBandwidth: Any
    videoBandwidth: Any
    originalVideoId: int | None
    originalAudioId: int | str
    originalTextId: Any
    originalImageId: Any


class AppMetadata(BaseModel):
    identifier: str
    downloaded: str


class StoredContentItem(BaseModel):
    offlineUri: str
    originalManifestUri: str
    duration: float
    size: int
    expiration: Any
    tracks: list[Track]
    appMetadata: AppMetadata
    isIncomplete: bool


class VideoItem(BaseModel):
    name: str
    shortName: str
    iconUri: str
    manifestUri: str
    source: str
    focus: bool
    disabled: bool
    extraText: list[ExtraTextItem]
    certificateUri: Any
    description: Optional[str]
    isFeatured: bool
    drm: list[str]
    features: list[str]
    licenseServers: LicenseServers
    licenseRequestHeaders: LicenseRequestHeaders
    requestFilter: Any | None = None
    responseFilter: Any | None = None
    clearKeys: dict[str, Any]
    extraConfig: ExtraConfigItem | None
    adTagUri: str | None
    imaVideoId: str | None
    imaAssetKey: str | None
    imaContentSrcId: int | None
    mimeType: Any
    mediaPlaylistFullMimeType: str | None
    storedProgress: int
    storedContent: Optional[Optional[StoredContentItem]] = None


class Videos(BaseModel):
    __root__: list[VideoItem]
