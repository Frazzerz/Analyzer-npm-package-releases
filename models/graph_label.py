from dataclasses import dataclass

@dataclass
class GraphLabel:
    """Class containing labels and titles for graphing metrics evolution"""

    # VersionMetrics : (AggregateVersionMetrics, label)
    METRICS = {
        'EVASION_TECHNIQUES': {
            'title': 'Evasion techniques metrics',
            'metrics': {
                'obfuscation_patterns_count': ('avg_obfuscation_patterns_count', 'Total count obfuscation patterns'),
                'platform_detections_count': ('avg_platform_detections_count', 'Total count platform detections'),
            }
        },
        'PAYLOAD_DELIVERY_EXECUTION': {
            'title': 'Payload delivery & Execution metrics',
            'metrics': {
                'timing_delays_count': ('avg_timing_delays_count', 'Total count timing delays'),
                'eval_count': ('avg_eval_count', 'Total count eval calls'),
                'shell_commands_count': ('avg_shell_commands_count', 'Total count shell commands'),
            }
        },
        'DATA_EXFILTRATION_C2': {
            'title': 'Data exfiltration & C2 metrics',
            'metrics': {
                'scan_functions_count': ('avg_scan_functions_count', 'Total count scan functions'),
                'sensitive_elements_count': ('avg_sensitive_elements_count', 'Total count sensitive elements'),
                'data_transmission_count': ('avg_data_transmission_count', 'Total count data transmissions'),
            }
        },
        'CRYPTOJACKING_WALLET_THEFT': {
            'title': 'Cryptojacking & Wallet theft metrics',
            'metrics': {
                'crypto_addresses': ('avg_crypto_addresses', 'Total count crypto addresses'),
                'cryptocurrency_name': ('avg_cryptocurrency_name', 'Total count cryptocurrency names'),
                'wallet_detection': ('avg_wallet_detection', 'Total count wallet detections'),
                'replaced_crypto_addresses': ('avg_replaced_crypto_addresses', 'Total count replaced addresses'),
                'hook_provider': ('avg_hook_provider', 'Total count hook providers'),
            }
        },
        'ACCOUNT_COMPROMISE': {
            'title': 'Account compromise & Integrity anomalies',
            'metrics': {
                'npm_maintainers': ('avg_npm_maintainers', 'Total count NPM maintainers'),
            }
        },
        'OTHER_METRICS': {
            'title': 'Other metrics',
            'metrics': {
                'total_files': ('avg_total_files', 'Total files'),
                'total_size_bytes': ('avg_total_size_bytes', 'Total size (bytes)'),
                'weighted_avg_blank_space_and_character_ratio': ('weighted_avg_blank_space_and_character_ratio', 'Weighted avg blank space ratio'),
                'weighted_avg_shannon_entropy': ('weighted_avg_shannon_entropy', 'Weighted avg Shannon entropy'),
                'longest_line_length': ('avg_longest_line_length', 'Longest line length'),
            }
        }
    }