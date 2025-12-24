from dataclasses import dataclass

@dataclass
class GraphLabel:
    """Class containing labels and titles for graphing metrics evolution"""
    METRIC_LABELS = {
        'obfuscation_patterns_count': 'Obfuscation Patterns',
        'longest_line_length': 'Longest Line Length',
        'platform_detections_count': 'Platform Detections',
        'timing_delays_count': 'Timing Delays',
        'eval_count': 'Eval Calls',
        'shell_commands_count': 'Shell Commands',
        'file_size_bytes': 'File Size (bytes)',
        'scan_functions_count': 'Scan Functions',
        'sensitive_elements_count': 'Sensitive Elements',
        'crypto_addresses': 'Crypto Addresses',
        'cryptocurrency_name': 'Cryptocurrency Names',
        'wallet_detection': 'Wallet Detections',
        'replaced_crypto_addresses': 'Replaced Addresses',
        'hook_provider': 'Hook Provider',
        'npm_maintainers': 'NPM Maintainers'
    }
    
    # Titles for each class
    CLASS_TITLES = {
        'EVASION_TECHNIQUES': 'Evasion Techniques Metrics',
        'PAYLOAD_DELIVERY_EXECUTION': 'Payload Delivery & Execution Metrics',
        'DATA_EXFILTRATION_C2': 'Data Exfiltration & C2 Metrics',
        'CRYPTOJACKING_WALLET_THEFT': 'Cryptojacking & Wallet Theft Metrics',
        'ACCOUNT_COMPROMISE': 'Account Compromise & Integrity Anomalies'
    }
    
    # Colors for lines (cycled for many metrics)
    COLOR_PALETTE = [
        '#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd',
        '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf',
        '#1a55FF', '#FF5733', '#33FF57', '#FF33F6', '#33FFF6'
    ]