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
