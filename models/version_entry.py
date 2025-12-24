from dataclasses import dataclass
from packaging.version import Version

@dataclass
class VersionEntry:
    version: Version
    name: str          # es. v1.1.2 o 1.1.1-local
    source: str        # "git" | "local"
    ref: object        # Tag git oppure Path locale
