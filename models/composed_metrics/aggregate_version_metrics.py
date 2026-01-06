from dataclasses import dataclass, field
from .aggregate_metrics.generic_aggregate import GenericAggregate
from .aggregate_metrics.evasion_aggregate import EvasionAggregate
from .aggregate_metrics.payload_aggregate import PayloadAggregate
from .aggregate_metrics.exfiltration_aggregate import ExfiltrationAggregate
from .aggregate_metrics.crypto_aggregate import CryptoAggregate
from .aggregate_metrics.account import AccountAggregate

@dataclass
class AggregateVersionMetrics:
    """Aggregated metrics across multiple package versions"""
    package: str = ""
    versions: str = ""
    generic: GenericAggregate = field(default_factory=GenericAggregate)
    evasion: EvasionAggregate = field(default_factory=EvasionAggregate)
    payload: PayloadAggregate = field(default_factory=PayloadAggregate)
    exfiltration: ExfiltrationAggregate = field(default_factory=ExfiltrationAggregate)
    crypto: CryptoAggregate = field(default_factory=CryptoAggregate)
    account: AccountAggregate = field(default_factory=AccountAggregate)

'''
@dataclass
class AggregateVersionMetrics:
    """Aggregated metrics across multiple package versions"""
    def __init__(self):
        self.package = ""
        self.versions = ""
        
        self.avg_obfuscation_patterns_count = 0
        self.avg_platform_detections_count = 0

        self.avg_timing_delays_count = 0
        self.avg_eval_count = 0
        self.avg_shell_commands_count = 0

        self.avg_scan_functions_count = 0
        self.avg_sensitive_elements_count = 0
        self.avg_data_transmission_count = 0

        self.avg_crypto_addresses = 0
        self.avg_cryptocurrency_name = 0
        self.avg_wallet_detection = 0
        self.avg_replaced_crypto_addresses = 0
        self.avg_hook_provider = 0
        
        self.avg_npm_maintainers = 0
        
        self.avg_total_files = 0
        self.avg_total_size_bytes = 0
        self.avg_total_size_chars = 0
        self.weighted_avg_blank_space_and_character_ratio = 0.0
        self.weighted_avg_shannon_entropy = 0.0
        self.avg_longest_line_length = 0

    package: str
    versions: str

    avg_obfuscation_patterns_count: int
    avg_platform_detections_count: int

    avg_timing_delays_count: int
    avg_eval_count: int
    avg_shell_commands_count: int

    avg_scan_functions_count: int
    avg_sensitive_elements_count: int
    avg_data_transmission_count: int

    avg_crypto_addresses: int
    avg_cryptocurrency_name: int
    avg_wallet_detection: int
    avg_replaced_crypto_addresses: int
    avg_hook_provider: int

    avg_npm_maintainers: int

    avg_total_files: int
    avg_total_size_bytes: bytes
    avg_total_size_chars: int
    weighted_avg_blank_space_and_character_ratio: float
    weighted_avg_shannon_entropy: float
    avg_longest_line_length: int
'''