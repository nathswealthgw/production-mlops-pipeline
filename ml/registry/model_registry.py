from dataclasses import dataclass
from datetime import datetime, timezone


@dataclass
class RegistryRecord:
    version: str
    artifact_uri: str
    promoted_at: str


class InMemoryModelRegistry:
    def __init__(self) -> None:
        self.records: dict[str, RegistryRecord] = {}

    def promote(self, version: str, artifact_uri: str) -> RegistryRecord:
        record = RegistryRecord(
            version=version,
            artifact_uri=artifact_uri,
            promoted_at=datetime.now(tz=timezone.utc).isoformat(),
        )
        self.records[version] = record
        return record
