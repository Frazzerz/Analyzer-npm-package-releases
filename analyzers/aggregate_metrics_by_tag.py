from collections import defaultdict
from zipfile import Path
from models.metrics import FileMetrics
from models.version_metrics import VersionMetrics
from typing import List
from analyzers.categories import AccountAnalyzer
from utils import synchronized_print

class AggregateMetricsByTag:
    
    @staticmethod
    def aggregate_metrics_by_tag(metrics_list: List[FileMetrics], repo_path: Path, source: str) -> List[VersionMetrics]:
        """Aggregate metrics by tag. metrics_list is a list of FileMetrics"""

        # grouped is a dict with key (package, version) and value a list of FileMetrics. group by (package, version)
        grouped = defaultdict(list)
        for fm in metrics_list:
            grouped[(fm.package, fm.version)].append(fm)

        if len(grouped) != 1:
            synchronized_print(f"Warning: Expected metrics for a single (package, version), but got {len(grouped)}")
            return []

        # Gets the only dictionary entry, unpacks the key (package, version) and puts the FileMetrics list in metrics
        (package, version), metrics = next(iter(grouped.items()))

        # Calculate also metrics for account categories
        account = AccountAnalyzer(pkg_name=package)
        account_metrics = account.analyze(version, repo_path, source)
        
        version_metrics = []
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
            data_transmission_count=sum(fm.data_transmission_count for fm in metrics),
            
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
            file_size_chars=sum(fm.file_size_chars for fm in metrics),
            file_size_bytes=sum(fm.file_size_bytes for fm in metrics),
            # In this way the average is calculated over all files
            #avg_blank_space_and_character_ratio=mean(fm.blank_space_and_character_ratio for fm in metrics),
            # To calculate the average blank space ratio for the version, we need to calculate the weighted average based on character size
            avg_blank_space_and_character_ratio=sum(fm.blank_space_and_character_ratio * fm.file_size_chars for fm in metrics) / sum(fm.file_size_chars for fm in metrics) if sum(fm.file_size_chars for fm in metrics) > 0 else 0.0,
            longest_line_length=max(fm.longest_line_length for fm in metrics),
            # in this way the shannon entropy is averaged over all files
            #shannon_entropy=mean(fm.shannon_entropy for fm in metrics)
            # to calculate the shannon entropy of the version, we need to calculate the weighted average based on character size
            # Rappresent the average information content per byte of the entire version
            shannon_entropy=sum(fm.shannon_entropy * fm.file_size_chars for fm in metrics) / sum(fm.file_size_chars for fm in metrics) if sum(fm.file_size_chars for fm in metrics) > 0 else 0.0
        )

        version_metrics.append(vm)

        return version_metrics
    
    @staticmethod
    def aggregate_metrics_incremental(previous_metrics: List[VersionMetrics], current_metrics: List[VersionMetrics]) -> List[VersionMetrics]:
        
        if not previous_metrics and not current_metrics:
            return []

        # Initial case: no previous metrics
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
                data_transmission_count=first.data_transmission_count,

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
                file_size_chars=first.file_size_chars,
                file_size_bytes=first.file_size_bytes,
                avg_blank_space_and_character_ratio=first.avg_blank_space_and_character_ratio,
                longest_line_length=first.longest_line_length,
                shannon_entropy=first.shannon_entropy
            )

            aggregated._last_version = first.version
            aggregated._count = 1
            return [aggregated]

        # General case: aggregate previous and current metrics
        prev = previous_metrics[0]
        curr = current_metrics[0]
        n = getattr(prev, "_count")

        last_version = getattr(prev, "_last_version", prev.version)
        new_version_str = f"all up to {last_version} (included) + {curr.version} (included)"

        aggregated = VersionMetrics(
            package=prev.package,
            version=new_version_str,

            code_types=list(set(prev.code_types) | set(curr.code_types)),
            obfuscation_patterns_count=prev.obfuscation_patterns_count + (curr.obfuscation_patterns_count - prev.obfuscation_patterns_count) / (n + 1),
            platform_detections_count=prev.platform_detections_count + (curr.platform_detections_count - prev.platform_detections_count) / (n + 1),
            
            timing_delays_count=prev.timing_delays_count + (curr.timing_delays_count - prev.timing_delays_count) / (n + 1),
            eval_count=prev.eval_count + (curr.eval_count - prev.eval_count) / (n + 1),
            shell_commands_count=prev.shell_commands_count + (curr.shell_commands_count - prev.shell_commands_count) / (n + 1),
            list_preinstall_scripts=list(set(prev.list_preinstall_scripts) | set(curr.list_preinstall_scripts)),
            
            scan_functions_count=prev.scan_functions_count + (curr.scan_functions_count - prev.scan_functions_count) / (n + 1),
            sensitive_elements_count=prev.sensitive_elements_count + (curr.sensitive_elements_count - prev.sensitive_elements_count) / (n + 1),
            data_transmission_count=prev.data_transmission_count + (curr.data_transmission_count - prev.data_transmission_count) / (n + 1),
            
            crypto_addresses=prev.crypto_addresses + (curr.crypto_addresses - prev.crypto_addresses) / (n + 1),
            list_crypto_addresses=list(set(prev.list_crypto_addresses) | set(curr.list_crypto_addresses)),
            cryptocurrency_name=prev.cryptocurrency_name + (curr.cryptocurrency_name - prev.cryptocurrency_name) / (n + 1),
            wallet_detection=prev.wallet_detection + (curr.wallet_detection - prev.wallet_detection) / (n + 1),
            replaced_crypto_addresses=prev.replaced_crypto_addresses + (curr.replaced_crypto_addresses - prev.replaced_crypto_addresses) / (n + 1),
            hook_provider=prev.hook_provider + (curr.hook_provider - prev.hook_provider) / (n + 1),
            
            npm_maintainers=prev.npm_maintainers + (curr.npm_maintainers - prev.npm_maintainers) / (n + 1),
            # Keep the latest commit hashes and release date
            npm_hash_commit=curr.npm_hash_commit,
            github_hash_commit=curr.github_hash_commit,
            npm_release_date=curr.npm_release_date,
            
            total_files=prev.total_files + (curr.total_files - prev.total_files) / (n + 1),
            file_size_chars=prev.file_size_chars + (curr.file_size_chars - prev.file_size_chars) / (n + 1),
            file_size_bytes=prev.file_size_bytes + (curr.file_size_bytes - prev.file_size_bytes) / (n + 1),
            avg_blank_space_and_character_ratio=prev.avg_blank_space_and_character_ratio + (curr.avg_blank_space_and_character_ratio - prev.avg_blank_space_and_character_ratio) / (n + 1),
            longest_line_length=prev.longest_line_length + (curr.longest_line_length - prev.longest_line_length) / (n + 1),
            shannon_entropy=prev.shannon_entropy + (curr.shannon_entropy - prev.shannon_entropy) / (n + 1)

        )
        aggregated._last_version = curr.version
        aggregated._count = n + 1
        return [aggregated]