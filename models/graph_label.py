from dataclasses import dataclass

@dataclass
class GraphLabel:
    """Class containing labels and titles for graphing metrics evolution"""

    METRICS = {
        'EVASION_TECHNIQUES': {
            'title': 'Evasion techniques metrics',
            'metrics': {
                'obfuscation_patterns_count': 'Obfuscation patterns',
                'platform_detections_count': 'Platform detections',
            }
        },
        'PAYLOAD_DELIVERY_EXECUTION': {
            'title': 'Payload delivery & Execution metrics',
            'metrics': {
                'timing_delays_count': 'Timing delays',
                'eval_count': 'Eval calls',
                'shell_commands_count': 'Shell commands',
            }
        },
        'DATA_EXFILTRATION_C2': {
            'title': 'Data exfiltration & C2 metrics',
            'metrics': {
                'scan_functions_count': 'Scan functions',
                'sensitive_elements_count': 'Sensitive elements',
                'data_transmission_count': 'Data transmissions',
            }
        },
        'CRYPTOJACKING_WALLET_THEFT': {
            'title': 'Cryptojacking & Wallet theft metrics',
            'metrics': {
                'crypto_addresses': 'Crypto addresses',
                'cryptocurrency_name': 'Cryptocurrency names',
                'wallet_detection': 'Wallet detections',
                'replaced_crypto_addresses': 'Replaced addresses',
                'hook_provider': 'Hook provider',
            }
        },
        'ACCOUNT_COMPROMISE': {
            'title': 'Account compromise & Integrity anomalies',
            'metrics': {
                'npm_maintainers': 'NPM maintainers',
            }
        },
        'OTHER_METRICS': {
            'title': 'Other metrics',
            'metrics': {
                'file_size_bytes': 'File size (bytes)',
                'avg_blank_space_ratio': 'Average blank space and character ratio',
                'shannon_entropy': 'Shannon entropy',
                'longest_line_length': 'Longest line length',
            }
        }
    }
    
    COLOR_PALETTE = [
        '#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd',
        '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf',
        '#1a55FF', '#FF5733', '#33FF57', '#FF33F6', '#33FFF6'
    ]