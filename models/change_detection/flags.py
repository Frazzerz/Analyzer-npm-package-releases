from dataclasses import dataclass, field
from .account_changes import AccountChanges
from .crypto_changes import CryptoChanges
from .exfiltration_changes import ExfiltrationChanges
from .evasion_changes import EvasionChanges
from .generic_changes import GenericChanges
from .payload_changes import PayloadChanges

@dataclass
class Flags:
    package: str
    version: str

    generic: GenericChanges = field(default_factory=GenericChanges)
    evasion: EvasionChanges = field(default_factory=EvasionChanges)
    payload: PayloadChanges = field(default_factory=PayloadChanges)
    exfiltration: ExfiltrationChanges = field(default_factory=ExfiltrationChanges)
    crypto: CryptoChanges = field(default_factory=CryptoChanges)
    account: AccountChanges = field(default_factory=AccountChanges)
'''
@dataclass
class Flags:
    """Flags indicating percentage differences or introductions across various metrics between versions (current vs all previous versions (or in some cases only previous version))"""
    package: str
    version: str

    # GENERIC METRICS
    percent_difference_total_files: float
    percent_difference_size_bytes: float
    percent_difference_weighted_avg_blank_space_and_character_ratio: float
    percent_difference_weighted_avg_shannon_entropy: float
    percent_difference_longest_line_length: float

    # EVASION TECHNIQUES
    obfuscated_code_introduced: bool
    minified_code_introduced: bool
    percent_difference_hex_obfuscation_patterns: float
    percent_difference_platform_detections: float

    # PAYLOAD DELIVERY & EXECUTION
    percent_difference_timing_delays: float
    percent_difference_eval_function: float
    percent_difference_shell_commands: float
    preinstall_scripts_introduced: bool
    preinstall_scripts_change: bool

    # DATA EXFILTRATION & C2
    percent_difference_scan_functions: float
    percent_difference_sensitive_elements: float
    percent_difference_data_transmission: float

    # CRYPTOJACKING & WALLET THEFT
    percent_difference_crypto_addresses: float
    change_crypto_addresses: bool
    percent_difference_cryptocurrency_name: float
    percent_difference_wallet_checks: float
    percent_difference_replaced_crypto_addresses: float
    percent_difference_hook_provider: float

    # ACCOUNT COMPROMISE & RELEASE INTEGRITY ANOMALIES
    #npm_new_maintainer: bool
    #npm_awakening_inactive_maintainer: bool
    #npm_new_maintainer_published_first_time_releases: bool
    #github_new_contributors: bool
    #hash_mismatch_commit_between_npm_and_github: bool  # no more github hash commit collected
    #npm_before_github: bool            # test
    #anomalous_time: bool
    package_reactivation: bool
'''