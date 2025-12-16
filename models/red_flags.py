from dataclasses import dataclass

@dataclass
class RedFlag:
    """Red flags indicating significant changes between two versions of a package"""
    package: str
    version_from: str
    version_to: str
    
    # EVASION TECHNIQUES
    obfuscated_code_introduced: bool
    minified_code_introduced: bool
    hex_suspicious_patterns_increase_significant: bool
    platform_detections_increase_significant: bool

    # PAYLOAD DELIVERY & EXECUTION
    timing_delays_increase_significant: bool
    eval_function_introduced: bool
    eval_function_increase_significant: bool
    shell_commands_increase_significant: bool
    size_bytes_increase_significant: bool
    preinstall_scripts_introduced: bool
    preinstall_scripts_change: bool

    # DATA EXFILTRATION & C2
    scan_functions_increase_significant: bool
    sensitive_elements_increase_significant: bool
    #data_transmission_increase: bool

    # CRYPTOJACKING & WALLET THEFT
    crypto_addresses_introduced: bool
    crypto_addresses_increase: bool
    change_crypto_addresses: bool
    cryptocurrency_name_introduced: bool
    cryptocurrency_name_increase: bool
    wallet_checks_introduced: bool
    wallet_checks_increase: bool
    replaced_crypto_addresses_introduced: bool
    hook_provider_introduced: bool

    # ACCOUNT COMPROMISE & RELEASE INTEGRITY ANOMALIES
    #npm_new_maintainer: bool
    #npm_awakening_inactive_maintainer: bool
    #npm_new_maintainer_published_first_time_releases: bool
    #github_new_contributors: bool
    #github_publisher_release: bool
    #github_repository_owner: bool
    hash_mismatch_commit_between_npm_and_github: bool
    #npm_before_github: bool            # test
    #hash_mismatch_file_between_npm_and_github: bool
    #anomalous_time: bool
    package_reactivation: bool
    #dependency_issues_keywords: bool