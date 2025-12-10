from dataclasses import dataclass

@dataclass
class RedFlagChanges:
    """Changes between versions (introduction of red flags)"""
    package: str
    file_path: str
    version_from: str
    version_to: str
    
    # EVASION TECHNIQUES
    transformed_code_introduced: bool
    transformed_code_class_changed: bool
    inserting_new_code_transformed_differently: bool
    hex_suspicious_patterns_presence_significant: bool
    hex_suspicious_patterns_increase_significant: bool
    platform_detections_presence_significant: bool
    platform_detections_increase_significant: bool
    presence_of_concatenated_elements: bool

    # PAYLOAD DELIVERY & EXECUTION
    timing_delays_presence_significant: bool
    timing_delays_increase_significant: bool
    eval_function_presence_significant: bool
    eval_function_increase_significant: bool
    shell_commands_presence_significant: bool
    shell_commands_increase_significant: bool
    significant_initial_size_bytes: bool
    size_bytes_increase_significant: bool
    preinstall_scripts_introduced: bool
    preinstall_scripts_increase: bool
    suspicious_dependency_introduced: bool

    # DATA EXFILTRATION & C2
    scan_functions_presence_significant: bool
    scan_functions_increase_significant: bool
    sensitive_elements_presence_significant: bool
    sensitive_elements_increase_significant: bool
    data_transmission_introduced: bool
    data_transmission_increase: bool

    # CRYPTOJACKING & WALLET THEFT
    initial_presence_of_crypto_addresses: bool
    crypto_addresses_introduced: bool
    crypto_addresses_increase: bool
    #---
    change_crypto_addresses: bool
    #---
    initial_presence_of_wallet_checks: bool
    wallet_checks_introduced: bool
    wallet_checks_increase: bool
    #---
    initial_presence_of_cryptocurrency_name: bool
    cryptocurrency_name_introduced: bool
    cryptocurrency_name_increase: bool
    #---
    replaced_crypto_addresses_introduced: bool
    #---
    hook_provider_introduced: bool

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