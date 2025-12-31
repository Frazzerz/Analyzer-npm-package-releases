from zipfile import Path
from models import FileMetrics, VersionMetrics, AggregateVersionMetrics
from typing import List
from analyzers.categories import AccountAnalyzer
from utils import synchronized_print

class AggregateMetricsByTag:

    @staticmethod
    def aggregate_metrics_by_tag(metrics_list: List[FileMetrics], repo_path: Path, source: str) -> VersionMetrics:
        """Aggregation of all metrics from the all files in the current version into a single VersionMetrics object"""

        if not metrics_list:
            synchronized_print("Warning: Empty metrics list provided to aggregate_metrics_by_tag")
            return None

        version_metrics = VersionMetrics()
        version_metrics.package = metrics_list[0].package
        version_metrics.version = metrics_list[0].version

        # Calculate metrics for account categories
        account = AccountAnalyzer(pkg_name=version_metrics.package)
        account_metrics = account.analyze(version_metrics.version, repo_path, source)
        version_metrics.npm_maintainers = account_metrics.get('npm_maintainers')
        version_metrics.npm_hash_commit = account_metrics.get('npm_hash_commit')
        version_metrics.github_hash_commit = account_metrics.get('github_hash_commit')
        version_metrics.npm_release_date = account_metrics.get('npm_release_date')
    
        # Calculate total file sizes for weighted averages
        for fm in metrics_list:
                # Filter for deobfuscated files, I don't consider the deobfuscated files for these metrics below
                if fm.code_type != "Deobfuscated":
                    version_metrics.total_size_chars += fm.file_size_chars
                    version_metrics.code_types.append(fm.code_type)
                    version_metrics.total_files += 1
                    version_metrics.total_size_bytes += fm.file_size_bytes
                    version_metrics.longest_line_length = max(version_metrics.longest_line_length, fm.longest_line_length)

        for fm in metrics_list:
            version_metrics.obfuscation_patterns_count += fm.obfuscation_patterns_count
            version_metrics.platform_detections_count += fm.platform_detections_count

            version_metrics.timing_delays_count += fm.timing_delays_count
            version_metrics.eval_count += fm.eval_count
            version_metrics.shell_commands_count += fm.shell_commands_count
            version_metrics.preinstall_scripts.extend(fm.preinstall_scripts)

            version_metrics.scan_functions_count += fm.scan_functions_count
            version_metrics.sensitive_elements_count += fm.sensitive_elements_count
            version_metrics.data_transmission_count += fm.data_transmission_count

            version_metrics.crypto_addresses += fm.crypto_addresses
            version_metrics.list_crypto_addresses.extend(fm.list_crypto_addresses)
            version_metrics.cryptocurrency_name += fm.cryptocurrency_name
            version_metrics.wallet_detection += fm.wallet_detection
            version_metrics.replaced_crypto_addresses += fm.replaced_crypto_addresses
            version_metrics.hook_provider += fm.hook_provider
            
            # weighted averages
            if fm.code_type != "Deobfuscated":
                # To calculate the average blank space ratio for the version, we need to calculate the weighted average based on character size,
                # so a larger file will have a larger weight on average
                version_metrics.weighted_avg_blank_space_and_character_ratio += fm.blank_space_and_character_ratio * fm.file_size_chars / version_metrics.total_size_chars if version_metrics.total_size_chars > 0 else 0.0
                # To calculate the shannon entropy of the version, we need to calculate the weighted average based on character size,
                # represent the average information content per character in the version
                version_metrics.weighted_avg_shannon_entropy += fm.shannon_entropy * fm.file_size_chars / version_metrics.total_size_chars if version_metrics.total_size_chars > 0 else 0.0

        # Remove duplicates in lists (set function)
        version_metrics.code_types = list(set(version_metrics.code_types))

        return version_metrics

    @staticmethod
    def aggregate_metrics_incremental(all_previous_metrics: AggregateVersionMetrics, current_metrics: VersionMetrics, count_versions: int, last_version: str) -> AggregateVersionMetrics:
        
        if not current_metrics:
            synchronized_print("Warning: Empty current metrics provided to aggregate_metrics_incremental")
            return None

        c = current_metrics
        # First version case
        if count_versions == 0:
            all_previous_metrics.package = c.package
            all_previous_metrics.versions = c.version

            all_previous_metrics.avg_obfuscation_patterns_count = c.obfuscation_patterns_count
            all_previous_metrics.avg_platform_detections_count = c.platform_detections_count
            
            all_previous_metrics.avg_timing_delays_count = c.timing_delays_count
            all_previous_metrics.avg_eval_count = c.eval_count
            all_previous_metrics.avg_shell_commands_count = c.shell_commands_count
            
            all_previous_metrics.avg_scan_functions_count = c.scan_functions_count
            all_previous_metrics.avg_sensitive_elements_count = c.sensitive_elements_count
            all_previous_metrics.avg_data_transmission_count = c.data_transmission_count
            
            all_previous_metrics.avg_crypto_addresses = c.crypto_addresses
            all_previous_metrics.avg_cryptocurrency_name = c.cryptocurrency_name
            all_previous_metrics.avg_wallet_detection = c.wallet_detection
            all_previous_metrics.avg_replaced_crypto_addresses = c.replaced_crypto_addresses
            all_previous_metrics.avg_hook_provider = c.hook_provider
            
            all_previous_metrics.avg_npm_maintainers = c.npm_maintainers
            
            all_previous_metrics.avg_total_files = c.total_files
            all_previous_metrics.avg_total_size_bytes = c.total_size_bytes
            all_previous_metrics.avg_total_size_chars = c.total_size_chars
            all_previous_metrics.weighted_avg_blank_space_and_character_ratio = c.weighted_avg_blank_space_and_character_ratio
            all_previous_metrics.weighted_avg_shannon_entropy = c.weighted_avg_shannon_entropy
            all_previous_metrics.avg_longest_line_length = c.longest_line_length
            
            return all_previous_metrics

        # General case: aggregate previous and current metrics
        n = count_versions

        all_previous_metrics.versions = f"all up to {last_version} (included) + {c.version} (included)"

        all_previous_metrics.avg_obfuscation_patterns_count = all_previous_metrics.avg_obfuscation_patterns_count + (c.obfuscation_patterns_count - all_previous_metrics.avg_obfuscation_patterns_count) / (n + 1)
        all_previous_metrics.avg_platform_detections_count = all_previous_metrics.avg_platform_detections_count + (c.platform_detections_count - all_previous_metrics.avg_platform_detections_count) / (n + 1)

        all_previous_metrics.avg_timing_delays_count = all_previous_metrics.avg_timing_delays_count + (c.timing_delays_count - all_previous_metrics.avg_timing_delays_count) / (n + 1)
        all_previous_metrics.avg_eval_count = all_previous_metrics.avg_eval_count + (c.eval_count - all_previous_metrics.avg_eval_count) / (n + 1)
        all_previous_metrics.avg_shell_commands_count = all_previous_metrics.avg_shell_commands_count + (c.shell_commands_count - all_previous_metrics.avg_shell_commands_count) / (n + 1)

        all_previous_metrics.avg_scan_functions_count = all_previous_metrics.avg_scan_functions_count + (c.scan_functions_count - all_previous_metrics.avg_scan_functions_count) / (n + 1)
        all_previous_metrics.avg_sensitive_elements_count = all_previous_metrics.avg_sensitive_elements_count + (c.sensitive_elements_count - all_previous_metrics.avg_sensitive_elements_count) / (n + 1)
        all_previous_metrics.avg_data_transmission_count = all_previous_metrics.avg_data_transmission_count + (c.data_transmission_count - all_previous_metrics.avg_data_transmission_count) / (n + 1)
        
        all_previous_metrics.avg_crypto_addresses = all_previous_metrics.avg_crypto_addresses + (c.crypto_addresses - all_previous_metrics.avg_crypto_addresses) / (n + 1)
        all_previous_metrics.avg_cryptocurrency_name = all_previous_metrics.avg_cryptocurrency_name + (c.cryptocurrency_name - all_previous_metrics.avg_cryptocurrency_name) / (n + 1)
        all_previous_metrics.avg_wallet_detection = all_previous_metrics.avg_wallet_detection + (c.wallet_detection - all_previous_metrics.avg_wallet_detection) / (n + 1)
        all_previous_metrics.avg_replaced_crypto_addresses = all_previous_metrics.avg_replaced_crypto_addresses + (c.replaced_crypto_addresses - all_previous_metrics.avg_replaced_crypto_addresses) / (n + 1)
        all_previous_metrics.avg_hook_provider = all_previous_metrics.avg_hook_provider + (c.hook_provider - all_previous_metrics.avg_hook_provider) / (n + 1)

        all_previous_metrics.avg_npm_maintainers = all_previous_metrics.avg_npm_maintainers + (c.npm_maintainers - all_previous_metrics.avg_npm_maintainers) / (n + 1)
        
        all_previous_metrics.avg_total_files = all_previous_metrics.avg_total_files + (c.total_files - all_previous_metrics.avg_total_files) / (n + 1)
        all_previous_metrics.avg_total_size_chars = all_previous_metrics.avg_total_size_chars + (c.total_size_chars - all_previous_metrics.avg_total_size_chars) / (n + 1)
        all_previous_metrics.avg_total_size_bytes = all_previous_metrics.avg_total_size_bytes + (c.total_size_bytes - all_previous_metrics.avg_total_size_bytes) / (n + 1)
        all_previous_metrics.weighted_avg_blank_space_and_character_ratio = all_previous_metrics.weighted_avg_blank_space_and_character_ratio + (c.weighted_avg_blank_space_and_character_ratio - all_previous_metrics.weighted_avg_blank_space_and_character_ratio) / (n + 1)
        all_previous_metrics.avg_longest_line_length = all_previous_metrics.avg_longest_line_length + (c.longest_line_length - all_previous_metrics.avg_longest_line_length) / (n + 1)
        all_previous_metrics.weighted_avg_shannon_entropy = all_previous_metrics.weighted_avg_shannon_entropy + (c.weighted_avg_shannon_entropy - all_previous_metrics.weighted_avg_shannon_entropy) / (n + 1)

        return all_previous_metrics