from dataclasses import dataclass

@dataclass
class RedFlagChanges:
    """Changes between versions (introduction of red flags)"""
    package: str
    file_path: str
    version_from: str
    version_to: str
    
    # EVASION TECHNIQUES
    obfuscation_introduced: bool
    obfuscation_class_changed: bool
    new_code_obfuscated_differently: bool
    timing_delays_introduced: bool
    dynamic_imports_introduced: bool
    env_detection_introduced: bool
    platform_detection_introduced: bool
    time_detection_introduced: bool

    # PAYLOAD DELIVERY & EXECUTION
    eval_shell_introduced: bool
    new_files_added_inside_pkg: bool
    size_increase_significant: bool
    dependency_suspicious_pkg_added_few_downloads: bool
    dependency_suspicious_pkg_added_just_created: bool
    dependency_suspicious_pkg_added_typesquatted: bool

    # DATA EXFILTRATION & C2
    tcp_udp_introduced: bool
    http_requests_introduced: bool
    suspicious_domains_introduced: bool
    sensitive_reads_introduced: bool
    directory_traversal_introduced: bool

    # CRYPTOJACKING & WALLET THEFT
    crypto_addresses_introduced: bool
    wallet_checks_introduced: bool

    # ACCOUNT COMPROMISE
    npm_new_maintainer: bool
    npm_awakening_inactive_maintainer: bool
    npm_new_maintainer_published_first_time_releases: bool
    npm_ownership_change: bool
    github_new_contributors: bool
    github_awakening_inactive_contributors: bool
    github_new_contributors_published_first_time_releases: bool
    github_ownership_change: bool

    # RELEASE INTEGRITY ANOMALIES
    npm_before_github: bool
    hash_mismatch_between_npm_and_github: bool
    anomalous_time: bool
    package_reactivation: bool
    dependency_issues_keywords: bool