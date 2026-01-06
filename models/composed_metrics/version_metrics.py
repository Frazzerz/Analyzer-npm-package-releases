from dataclasses import dataclass, field
from .aggregate_metrics.generic_aggregate import GenericVersion
from .aggregate_metrics.evasion_aggregate import EvasionVersion
from .aggregate_metrics.payload_aggregate import PayloadVersion
from .aggregate_metrics.exfiltration_aggregate import ExfiltrationVersion
from .aggregate_metrics.crypto_aggregate import CryptoVersion
from .aggregate_metrics.account import AccountVersion

@dataclass
class VersionMetrics:
    """Aggregated metrics for a specific package version"""
    package: str = ""
    version: str = ""
    
    generic: GenericVersion = field(default_factory=GenericVersion)
    evasion: EvasionVersion = field(default_factory=EvasionVersion)
    payload: PayloadVersion = field(default_factory=PayloadVersion)
    exfiltration: ExfiltrationVersion = field(default_factory=ExfiltrationVersion)
    crypto: CryptoVersion = field(default_factory=CryptoVersion)
    account: AccountVersion = field(default_factory=AccountVersion)
'''
@dataclass
class VersionMetrics:
    """Aggregated metrics for a specific package version"""
    def __init__(self):
        self.package = ""
        self.version = ""
        
        self.code_types = []
        self.obfuscation_patterns_count = 0
        self.platform_detections_count = 0

        self.timing_delays_count = 0
        self.eval_count = 0
        self.shell_commands_count = 0
        self.preinstall_scripts = []

        self.scan_functions_count = 0
        self.sensitive_elements_count = 0
        self.data_transmission_count = 0

        self.crypto_addresses = 0
        self.list_crypto_addresses = []
        self.cryptocurrency_name = 0
        self.wallet_detection = 0
        self.replaced_crypto_addresses = 0
        self.hook_provider = 0
        
        # ACCOUNT COMPROMISE & RELEASE INTEGRITY ANOMALIES
        self.npm_maintainers = 0
        self.npm_hash_commit = ""
        self.github_hash_commit = ""
        self.npm_release_date = ""
        
        # GENERIC METRICS
        self.total_files = 0
        self.total_size_bytes = 0
        self.total_size_chars = 0
        self.weighted_avg_blank_space_and_character_ratio = 0.0
        self.weighted_avg_shannon_entropy = 0.0
        self.longest_line_length = 0

    package: str
    version: str

    code_types: List[str]
    obfuscation_patterns_count: int
    platform_detections_count: int

    timing_delays_count: int
    eval_count: int
    shell_commands_count: int
    preinstall_scripts: List[str]

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
    total_size_bytes: bytes
    total_size_chars: int
    weighted_avg_blank_space_and_character_ratio: float
    weighted_avg_shannon_entropy: float
    longest_line_length: int
'''