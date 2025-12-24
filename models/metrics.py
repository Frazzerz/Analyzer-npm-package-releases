from dataclasses import dataclass
from typing import List

@dataclass
class FileMetrics:
    """Metrics for a single file, all int variables represent counts, unless otherwise specified"""
    package: str
    version: str
    file_path: str
    
    # EVASION TECHNIQUES
    code_type: str
    obfuscation_patterns_count: int
    list_obfuscation_patterns: List[str]
    longest_line_length: int
    blank_space_and_character_ratio: float
    platform_detections_count: int
    list_platform_detections: List[str]
    
    # PAYLOAD DELIVERY & EXECUTION
    timing_delays_count: int
    list_timing_delays: List[str]
    eval_count: int
    eval_list: List[str]
    shell_commands_count: int
    list_shell_commands: List[str]
    file_size_bytes: int
    preinstall_scripts: bool
    list_preinstall_scripts: List[str]

    # DATA EXFILTRATION & C2
    scan_functions_count: int
    list_scan_functions: List[str]
    sensitive_elements_count: int
    list_sensitive_elements: List[str]
    #data_transmission_count: int
    #list_data_transmission: List[str]
    
    # CRYPTOJACKING & WALLET THEFT
    crypto_addresses: int
    list_crypto_addresses: List[str]
    cryptocurrency_name: int
    wallet_detection: int
    wallet_detection_list: List[str]
    replaced_crypto_addresses: int
    replaced_crypto_addresses_list: List[str]
    hook_provider: int

    # ACCOUNT COMPROMISE & RELEASE INTEGRITY ANOMALIES
    ##npm_maintainers: int
    ##npm_maintainers_nicks: List[str]
    ##npm_maintainers_emails: List[str]
    ##npm_maintainer_published_release: str
    #github_contributors: int
    #github_contributors_nicks: List[str]
    #github_contributors_emails: List[str]
    #github_publisher_release: str
    #github_repository_owner: str
    ##npm_hash_commit: str
    ##github_hash_commit: str
    ##npm_hash_file: str
    #github_hash_file: str
    ##npm_release_date: str
    #'github_release_date': str
    #malicious_issues: int