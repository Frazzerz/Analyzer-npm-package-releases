from dataclasses import dataclass

@dataclass
class VersionEntry:
    '''Represents a specific version entry of a package'''
    #version: str
    name: str          # e.g. v1.1.2, 1.1.1+local or posthog-node@5.18.0
    source: str        # "git", "local", "deobfuscated", "tarball"
    ref: object        # Local Path or Git TagReference