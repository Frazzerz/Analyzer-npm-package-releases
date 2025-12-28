from dataclasses import dataclass
from packaging.version import Version

@dataclass
class VersionEntry:
    '''Represents a specific version entry of a package'''
    version: Version
    name: str          # ex. v1.1.2 o 1.1.1-local
    source: str        # "git" or "local"
    ref: object        # Git Tag or Local Path