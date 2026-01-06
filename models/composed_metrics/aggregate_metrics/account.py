from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class AccountVersion:
    """For a single version"""
    npm_maintainers: int = 0
    npm_hash_commit: str = ""
    ##github_hash_commit: str = ""
    npm_release_date: Optional[datetime] = None

@dataclass
class AccountAggregate:
    """For aggregate versions"""
    avg_npm_maintainers: float = 0.0