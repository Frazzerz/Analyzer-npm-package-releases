from dataclasses import dataclass

@dataclass
class AggregateMetrics:

    METRIC_CLASSES = {
        'EVASION_TECHNIQUES': [
            'code_type',
            'obfuscation_patterns_count',
            'platform_detections_count'
        ],
        'PAYLOAD_DELIVERY_EXECUTION': [
            'timing_delays_count',
            'eval_count',
            'shell_commands_count',
            'list_preinstall_scripts'
        ],
        'DATA_EXFILTRATION_C2': [
            'scan_functions_count',
            'sensitive_elements_count'
        ],
        'CRYPTOJACKING_WALLET_THEFT': [
            'crypto_addresses',
            'list_crypto_addresses',
            'cryptocurrency_name',
            'wallet_detection',
            'replaced_crypto_addresses',
            'hook_provider'
        ],
        'ACCOUNT_COMPROMISE': [
            'npm_maintainers'
        ],
        'OTHER_METRICS': [
            'file_size_bytes',
            'avg_blank_space_ratio'
        ],
        'MAX_METRICS': [
            'longest_line_length'
        ]
    }