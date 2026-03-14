from __future__ import annotations

from typing import Dict


class ProvisioningItem:
    def __init__(
        self,
        version: int,
        addon_id: str,
        artifact_filename: str,
        target_dir: str,
    ):
        self.version = version
        self.addon_id = addon_id
        self.artifact_filename = artifact_filename
        self.target_dir = target_dir


class ProvisioningState:
    def __init__(self, installed_versions: Dict[str, Dict[str, int]] | None = None):
        self.installed_versions = installed_versions or {}

    @classmethod
    def from_dict(cls, data: dict) -> ProvisioningState:
        return cls(installed_versions=data)

    def to_dict(self) -> dict:
        return self.installed_versions

    def get_version(self, addon_id: str, artifact_filename: str) -> int:
        return self.installed_versions.get(addon_id, {}).get(artifact_filename, 0)

    def set_version(self, addon_id: str, artifact_filename: str, version: int):
        if addon_id not in self.installed_versions:
            self.installed_versions[addon_id] = {}
        self.installed_versions[addon_id][artifact_filename] = version
