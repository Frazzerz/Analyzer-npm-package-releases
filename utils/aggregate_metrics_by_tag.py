from collections import defaultdict
from models.metrics import FileMetrics
from typing import Any, List, Dict

class AggregateMetricsByTag:
    
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
            #'blank_space_and_character_ratio'  # TODO per plottarlo, ratio_versione = ( somma di tutti spazi di tutti i file) / (somma di tutti caratteri di tutti i file)
        ],
        'MAX_METRICS': [
            'longest_line_length'
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
    def aggregate_metrics_by_version(metrics_list: List[FileMetrics]) -> Dict[str, Dict[str, Any]]:
        """Aggregate metrics by version:
        - int are summed
        - list[str] are concatenated (duplicates allowed, order irrelevant)
        """
        aggregated: Dict[str, Dict[str, Any]] = defaultdict(dict)

        # Collect metric names once
        metric_names = []
        for class_metrics in AggregateMetricsByTag.METRIC_CLASSES.values():
            metric_names.extend(class_metrics)

        for metric in metrics_list:
            version = metric.version

            for metric_name in metric_names:
                value = getattr(metric, metric_name, None)
                if value is None:
                    continue

                # numeric aggregation
                if isinstance(value, (int, float)):
                    if metric_name in AggregateMetricsByTag.METRIC_CLASSES['MAX_METRICS']:
                        aggregated[version][metric_name] = max(aggregated[version].get(metric_name, value), value)
                    else:
                        aggregated[version].setdefault(metric_name, 0)
                        aggregated[version][metric_name] += value

                # list[str] aggregation (simple concatenation)
                elif isinstance(value, list):
                    aggregated[version].setdefault(metric_name, [])
                    aggregated[version][metric_name].extend(value)

                elif isinstance(value, str):
                    aggregated[version].setdefault(metric_name, [])
                    if value not in aggregated[version][metric_name]:
                        aggregated[version][metric_name].append(value)

        # Sort by version
        sorted_aggregated = {}
        for version in sorted(aggregated.keys(), key=AggregateMetricsByTag._version_sort_key):
            sorted_aggregated[version] = aggregated[version]

        return sorted_aggregated