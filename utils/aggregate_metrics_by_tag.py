from collections import defaultdict
from models.metrics import FileMetrics
from typing import List, Dict

class AggregateMetricsByTag:
    
    METRIC_CLASSES = {
        'EVASION_TECHNIQUES': [
            'suspicious_patterns_count',
            'longest_line_length',
            'platform_detections_count'
        ],
        'PAYLOAD_DELIVERY_EXECUTION': [
            'timing_delays_count',
            'eval_count',
            'shell_commands_count',
            'file_size_bytes'
        ],
        'DATA_EXFILTRATION_C2': [
            'scan_functions_count',
            'sensitive_elements_count'
        ],
        'CRYPTOJACKING_WALLET_THEFT': [
            'crypto_addresses',
            'cryptocurrency_name',
            'wallet_detection',
            'replaced_crypto_addresses',
            'hook_provider'
        ],
        'ACCOUNT_COMPROMISE': [
            'npm_maintainers'
        ]
    }

    @staticmethod
    def _normalize_version(version: str) -> str:
        """Normalize versions by removing prefixes and suffixes"""
        version = version.lstrip('v')
        version = version.replace('-local', '')
        return version

    @staticmethod
    def _version_sort_key(version: str):
        """Sort key for versions (supports semantic versions)"""
        normalized = AggregateMetricsByTag._normalize_version(version)
        parts = []
        for part in normalized.split('.'):
            try:
                if '-' in part:
                    main, suffix = part.split('-', 1)
                    parts.append((int(main), suffix))
                else:
                    parts.append((int(part), ''))
            except ValueError:
                parts.append((9999, part))
        return parts

    @staticmethod
    def aggregate_metrics_by_version(metrics_list: List[FileMetrics]) -> Dict[str, Dict[str, int]]:
        """Aggregate metrics by version, summing values from all files"""
        aggregated = defaultdict(lambda: defaultdict(int))
        
        for metric in metrics_list:
            version = metric.version
            
            # Collect all metrics from all classes
            all_metrics = []
            for class_metrics in AggregateMetricsByTag.METRIC_CLASSES.values():
                all_metrics.extend(class_metrics)
            
            for metric_name in all_metrics:
                value = getattr(metric, metric_name, 0)
                if isinstance(value, (int, float)):
                    aggregated[version][metric_name] += value
        
        # Sort the aggregated dictionary by version
        sorted_aggregated = {}
        for version in sorted(aggregated.keys(), key=AggregateMetricsByTag._version_sort_key):
            sorted_aggregated[version] = dict(aggregated[version])
        
        return sorted_aggregated