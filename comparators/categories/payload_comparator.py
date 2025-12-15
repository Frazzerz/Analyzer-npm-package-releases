from typing import Dict, Optional

class PayloadComparator:
    """Compare payload delivery & execution metrics between two versions (tags) to identify red flags"""
    
    def compare(self, prev_tag_metrics: Optional[Dict], curr_tag_metrics: Dict) -> Dict:
        
        if prev_tag_metrics is None:
            # No comparison for first version - return no flags
            return {
                'timing_delays_presence_significant': False,
                'timing_delays_increase_significant': False,
                'eval_function_initial_presence': False,
                'eval_function_introduced': False,
                'eval_function_increase_significant': False,
                'shell_commands_presence_significant': False,
                'shell_commands_increase_significant': False,
                'significant_initial_size_bytes': False,
                'size_bytes_increase_significant': False,
                'preinstall_initial_presence': False,
                'preinstall_scripts_introduced': False,
                'preinstall_scripts_change': False,
                #'suspicious_dependency_introduced': False,
            }
        else:
            # Existing tag
            prev_timing = prev_tag_metrics.get('timing_delays_count')
            curr_timing = curr_tag_metrics.get('timing_delays_count')
            timing_increase = curr_timing - prev_timing

            prev_eval = prev_tag_metrics.get('eval_count')
            curr_eval = curr_tag_metrics.get('eval_count')
            eval_increase = curr_eval - prev_eval

            prev_shell = prev_tag_metrics.get('shell_commands_count')
            curr_shell = curr_tag_metrics.get('shell_commands_count')
            shell_increase = curr_shell - prev_shell

            prev_size = prev_tag_metrics.get('file_size_bytes')
            curr_size = curr_tag_metrics.get('file_size_bytes')

            prev_preinstall = prev_tag_metrics.get('preinstall_scripts', False)
            curr_preinstall = curr_tag_metrics.get('preinstall_scripts', False)

            return {
                'timing_delays_presence_significant': False,
                'timing_delays_increase_significant': (timing_increase >= 5 and timing_increase > prev_timing * 0.5),
                'eval_function_initial_presence': False,
                'eval_function_introduced': prev_eval == 0 and curr_eval > 0,
                'eval_function_increase_significant': (eval_increase >= 5 and eval_increase > prev_eval * 0.5 and prev_eval != 0),
                'shell_commands_presence_significant': False,
                'shell_commands_increase_significant': (shell_increase >= 5 and shell_increase > prev_shell * 0.5),
                'significant_initial_size_bytes': False,
                'size_bytes_increase_significant': curr_size > prev_size * 10,
                'preinstall_initial_presence': False,
                'preinstall_scripts_introduced': not prev_preinstall and curr_preinstall,
                'preinstall_scripts_change': False,
                #'suspicious_dependency_introduced': False,
            }
'''
    def compare(self, prev: FileMetrics, curr: FileMetrics) -> Dict:
        # New file
        if prev is None:
            return {
                'timing_delays_presence_significant': curr.timing_delays_count > 5,         # threshold
                'timing_delays_increase_significant': False,
                'eval_function_initial_presence': curr.eval_count > 0,
                'eval_function_introduced': False,
                'eval_function_increase_significant': False,
                'shell_commands_presence_significant': curr.shell_commands_count > 5,       # threshold
                'shell_commands_increase_significant': False,
                'significant_initial_size_bytes': curr.file_size_bytes > 1024 * 1024,        # 1 MB
                'size_bytes_increase_significant': False,
                'preinstall_initial_presence': curr.preinstall_scripts,
                'preinstall_scripts_introduced': False,
                'preinstall_scripts_change': False,
                #'suspicious_dependency_introduced': False,
            }
        else:
            # Existing file
            return {
                'timing_delays_presence_significant': False,
                # threshold, increase by at least more than 50% and at least the increase must be 5
                'timing_delays_increase_significant': ((increase := curr.timing_delays_count - prev.timing_delays_count) >= 5 and
                    increase > prev.timing_delays_count * 0.5 ),
                'eval_function_initial_presence': False,
                'eval_function_introduced': prev.eval_count == 0 and curr.eval_count > 0,
                'eval_function_increase_significant': ((increase := curr.eval_count - prev.eval_count) >= 5 and
                    increase > prev.eval_count * 0.5 and prev.eval_count != 0 ),
                'shell_commands_presence_significant': False,
                'shell_commands_increase_significant': ((increase := curr.shell_commands_count - prev.shell_commands_count) >= 5 and
                    increase > prev.shell_commands_count * 0.5 ),
                'significant_initial_size_bytes': False,
                'size_bytes_increase_significant': curr.file_size_bytes > prev.file_size_bytes * 10,                                 # 1000% increase
                'preinstall_initial_presence': False,
                'preinstall_scripts_introduced': not prev.preinstall_scripts and curr.preinstall_scripts,
                'preinstall_scripts_change': set(prev.list_preinstall_scripts) != set(curr.list_preinstall_scripts) and prev.preinstall_scripts,
                #'suspicious_dependency_introduced': False,
            }
'''