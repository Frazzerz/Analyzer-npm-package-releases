from collections import defaultdict
from zipfile import Path
from models.metrics import FileMetrics
from models.version_metrics import VersionMetrics
from typing import Any, List, Dict, Optional
from collections import defaultdict
from statistics import mean
from analyzers.categories import AccountAnalyzer
from utils import synchronized_print

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
    
    @staticmethod
    def aggregate_metrics_by_tag(metrics_list: List[FileMetrics], repo_path: Path, source: str) -> List[VersionMetrics]:
        """Aggregate metrics by tag (metric classes)"""

        grouped = defaultdict(list)

        # 1. raggruppo per (package, version)
        for fm in metrics_list:
            grouped[(fm.package, fm.version)].append(fm)

        version_metrics = []

        # 2. aggrego
        for (package, version), metrics in grouped.items():
            # Calculate also metrics for account categories
            account_metrics = AccountAnalyzer(pkg_name=package).analyze(package, version, repo_path, source)

            vm = VersionMetrics(
                package=package,
                version=version,

                code_types = list({fm.code_type for fm in metrics}),
                obfuscation_patterns_count=sum(fm.obfuscation_patterns_count for fm in metrics),
                platform_detections_count=sum(fm.platform_detections_count for fm in metrics),
                
                timing_delays_count=sum(fm.timing_delays_count for fm in metrics),
                eval_count=sum(fm.eval_count for fm in metrics),
                shell_commands_count=sum(fm.shell_commands_count for fm in metrics),
                list_preinstall_scripts=list({script for fm in metrics for script in fm.list_preinstall_scripts}),
                
                scan_functions_count=sum(fm.scan_functions_count for fm in metrics),
                sensitive_elements_count=sum(fm.sensitive_elements_count for fm in metrics),
                
                crypto_addresses=sum(fm.crypto_addresses for fm in metrics),
                list_crypto_addresses=list({addr for fm in metrics for addr in fm.list_crypto_addresses}),
                cryptocurrency_name=sum(fm.cryptocurrency_name for fm in metrics),
                wallet_detection=sum(fm.wallet_detection for fm in metrics),
                replaced_crypto_addresses=sum(fm.replaced_crypto_addresses for fm in metrics),
                hook_provider=sum(fm.hook_provider for fm in metrics),
                
                npm_maintainers=account_metrics.get('npm_maintainers'),
                npm_hash_commit=account_metrics.get('npm_hash_commit'),
                github_hash_commit=account_metrics.get('github_hash_commit'),
                npm_release_date=account_metrics.get('npm_release_date'),

                total_files= len(metrics),
                file_size_bytes=sum(fm.file_size_bytes for fm in metrics),
                avg_blank_space_ratio=mean(fm.blank_space_and_character_ratio for fm in metrics),
                longest_line_length=max(fm.longest_line_length for fm in metrics)
            )

            version_metrics.append(vm)

        return version_metrics
    
    @staticmethod
    def aggregate_metrics(metrics_list: dict[str, VersionMetrics]) -> List[VersionMetrics]:
        """Aggregate metrics across versions into a single VersionMetrics"""

        if not metrics_list:
            return []

        metrics = list(metrics_list.values())

        aggregated = VersionMetrics(
            package=metrics[0]["package"],
            version="all_prev_aggregated",

            code_types=list({ct for m in metrics for ct in m.get("code_types")}),
            obfuscation_patterns_count=sum(m.get("obfuscation_patterns_count") for m in metrics),
            platform_detections_count=sum(m.get("platform_detections_count") for m in metrics),

            timing_delays_count=sum(m.get("timing_delays_count") for m in metrics),
            eval_count=sum(m.get("eval_count") for m in metrics),
            shell_commands_count=sum(m.get("shell_commands_count") for m in metrics),
            list_preinstall_scripts=list({s for m in metrics for s in m.get("list_preinstall_scripts")}),

            scan_functions_count=sum(m.get("scan_functions_count") for m in metrics),
            sensitive_elements_count=sum(m.get("sensitive_elements_count") for m in metrics),
            
            crypto_addresses=sum(m.get("crypto_addresses") for m in metrics),
            list_crypto_addresses=list({a for m in metrics for a in m.get("list_crypto_addresses")}),
            cryptocurrency_name=sum(m.get("cryptocurrency_name") for m in metrics),
            wallet_detection=sum(m.get("wallet_detection") for m in metrics),
            replaced_crypto_addresses=sum(m.get("replaced_crypto_addresses") for m in metrics),
            hook_provider=sum(m.get("hook_provider") for m in metrics),
            
            npm_maintainers=mean(m.get("npm_maintainers") for m in metrics),
            npm_hash_commit=None, #metrics[-1].get("npm_hash_commit"),
            github_hash_commit=None, #metrics[-1].get("github_hash_commit"),
            npm_release_date=None, #metrics[-1].get("npm_release_date"),

            total_files=mean(m.get("total_files") for m in metrics),
            file_size_bytes=mean(m.get("file_size_bytes") for m in metrics),
            avg_blank_space_ratio=mean(m.get("avg_blank_space_ratio") for m in metrics),
            longest_line_length=mean(m.get("longest_line_length") for m in metrics),
        )

        return [aggregated]
    
    #@staticmethod
    #def aggregate_metrics_incremental(previous_metrics: List[VersionMetrics], current_metrics: List[VersionMetrics]) -> List[VersionMetrics]:
    #    """Aggregate previous metrics with current metrics incrementally"""
    #    return
    
    @staticmethod
    def aggregate_metrics_incremental(previous_metrics: List[VersionMetrics], current_metrics: List[VersionMetrics]) -> List[VersionMetrics]:
        
         # Nessun dato
        if not previous_metrics and not current_metrics:
            return []

        # 🔹 Caso iniziale: nessun precedente
        if not previous_metrics:
            first = current_metrics[0]

            aggregated = VersionMetrics(
                package=first.package,
                version=f"all up to {first.version} (included)",

                code_types=list(set(first.code_types)),
                obfuscation_patterns_count=first.obfuscation_patterns_count,
                platform_detections_count=first.platform_detections_count,
                timing_delays_count=first.timing_delays_count,
                eval_count=first.eval_count,
                shell_commands_count=first.shell_commands_count,
                list_preinstall_scripts=list(set(first.list_preinstall_scripts)),
                scan_functions_count=first.scan_functions_count,
                sensitive_elements_count=first.sensitive_elements_count,

                crypto_addresses=first.crypto_addresses,
                list_crypto_addresses=list(set(first.list_crypto_addresses)),
                cryptocurrency_name=first.cryptocurrency_name,
                wallet_detection=first.wallet_detection,
                replaced_crypto_addresses=first.replaced_crypto_addresses,
                hook_provider=first.hook_provider,

                npm_maintainers=first.npm_maintainers,
                npm_hash_commit=first.npm_hash_commit,
                github_hash_commit=first.github_hash_commit,
                npm_release_date=first.npm_release_date,

                total_files=first.total_files,
                file_size_bytes=first.file_size_bytes,
                avg_blank_space_ratio=first.avg_blank_space_ratio,
                longest_line_length=first.longest_line_length,
            )

            # Salvo la versione reale per le aggregazioni successive
            aggregated._last_real_version = first.version
            aggregated._count = 1
            return [aggregated]

        # 🔹 Aggregazione incrementale vera
        prev = previous_metrics[0]
        curr = current_metrics[0]
        n = getattr(prev, "_count", 1)

        # Versione corretta: ultima versione reale del precedente + versione corrente
        last_real_version = getattr(prev, "_last_real_version", prev.version)
        new_version_str = f"all up to {last_real_version} (included) + {curr.version} (included)"

        aggregated = VersionMetrics(
            package=prev.package,
            version=new_version_str,

            # ---- concatenazioni incrementali ----
            code_types=list(set(prev.code_types) | set(curr.code_types)),
            list_preinstall_scripts=list(
                set(prev.list_preinstall_scripts) | set(curr.list_preinstall_scripts)
            ),
            list_crypto_addresses=list(
                set(prev.list_crypto_addresses) | set(curr.list_crypto_addresses)
            ),

            # ---- somme incrementali ----
            obfuscation_patterns_count=prev.obfuscation_patterns_count + curr.obfuscation_patterns_count,
            platform_detections_count=prev.platform_detections_count + curr.platform_detections_count,
            timing_delays_count=prev.timing_delays_count + curr.timing_delays_count,
            eval_count=prev.eval_count + curr.eval_count,
            shell_commands_count=prev.shell_commands_count + curr.shell_commands_count,
            scan_functions_count=prev.scan_functions_count + curr.scan_functions_count,
            sensitive_elements_count=prev.sensitive_elements_count + curr.sensitive_elements_count,
            crypto_addresses=prev.crypto_addresses + curr.crypto_addresses,
            cryptocurrency_name=prev.cryptocurrency_name + curr.cryptocurrency_name,
            wallet_detection=prev.wallet_detection + curr.wallet_detection,
            replaced_crypto_addresses=prev.replaced_crypto_addresses + curr.replaced_crypto_addresses,
            hook_provider=prev.hook_provider + curr.hook_provider,

            # ---- medie incrementali ----
            npm_maintainers=prev.npm_maintainers + (curr.npm_maintainers - prev.npm_maintainers) / (n + 1),
            total_files=prev.total_files + (curr.total_files - prev.total_files) / (n + 1),
            file_size_bytes=prev.file_size_bytes + (curr.file_size_bytes - prev.file_size_bytes) / (n + 1),
            avg_blank_space_ratio=prev.avg_blank_space_ratio + (
                curr.avg_blank_space_ratio - prev.avg_blank_space_ratio
            ) / (n + 1),
            longest_line_length=prev.longest_line_length + (
                curr.longest_line_length - prev.longest_line_length
            ) / (n + 1),

            # ---- ultimo valore noto ----
            npm_hash_commit=curr.npm_hash_commit,
            github_hash_commit=curr.github_hash_commit,
            npm_release_date=curr.npm_release_date,
        )

        aggregated._last_real_version = curr.version
        aggregated._count = n + 1
        
        return [aggregated]