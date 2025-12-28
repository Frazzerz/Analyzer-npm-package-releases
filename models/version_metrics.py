from dataclasses import dataclass
from datetime import datetime
from typing import List

@dataclass
class VersionMetrics:
    """Aggregated metrics for a specific package version"""
    package: str
    version: str

    code_types: List[str]
    obfuscation_patterns_count: int
    platform_detections_count: int

    timing_delays_count: int
    eval_count: int
    shell_commands_count: int
    list_preinstall_scripts: List[str]

    scan_functions_count: int
    sensitive_elements_count: int
    data_transmission_count: int

    crypto_addresses: int
    list_crypto_addresses: List[str]
    cryptocurrency_name: int
    wallet_detection: int
    replaced_crypto_addresses: int
    hook_provider: int

    # ACCOUNT COMPROMISE & RELEASE INTEGRITY ANOMALIES
    npm_maintainers: int
    npm_hash_commit: str
    github_hash_commit: str
    npm_release_date: datetime

    # GENERIC METRICS
    total_files: int
    file_size_bytes: int
    avg_blank_space_ratio: float
    shannon_entropy: float
    longest_line_length: int