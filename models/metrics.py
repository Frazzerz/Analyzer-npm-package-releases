from dataclasses import dataclass
from typing import List

@dataclass
class FileMetrics:
    """Metrics for a single file, all int variables represent counts, unless otherwise specified"""
    package: str
    version: str
    file_path: str
    
    # EVASION TECHNIQUES
    is_obfuscated: bool
    obfuscation_type: str
    new_code_obfuscated_differently: bool
    timing_delays: int
    dynamic_imports: int
    env_node_env: int
    env_platform: int
    execution_time: int
    
    # PAYLOAD DELIVERY & EXECUTION
    eval: int
    shell_commands: int
    file_or_executable_inside_pkg: int
    file_size_bytes: int
    suspicious_dependencies_few_downloads: int
    suspicious_dependencies_just_created: int
    suspicious_dependencies_typesquatted: int
    
    # DATA EXFILTRATION & C2
    tcp_udp_sockets: int
    http_requests: int
    suspicious_domains: int
    sensitive_file_reads: int
    directory_traversal: int
    
    # CRYPTOJACKING & WALLET THEFT
    crypto_addresses: int
    wallet_detection: int

    # ACCOUNT COMPROMISE
    npm_maintainers: int
    npm_maintainers_nicks: List[str]
    npm_maintainers_emails: List[str]
    npm_maintainer_pubblished_release: str
    github_contributors: int
    github_contributors_nicks: List[str]
    github_contributors_emails: List[str]
    github_contributors_published_release: str
    github_owners: str

    # RELEASE INTEGRITY ANOMALIES
    npm_release_date: str
    github_release_date: str
    hash_github: str
    hash_npm: str
    malicious_issues: int