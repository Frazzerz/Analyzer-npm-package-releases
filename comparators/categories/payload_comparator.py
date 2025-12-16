from typing import Dict, Optional

class PayloadComparator:
    """Compare payload delivery & execution metrics between two versions (tags) to identify red flags"""
    
    def compare(self, prev_tag_metrics: Optional[Dict], curr_tag_metrics: Dict) -> Dict:
        
        if prev_tag_metrics is None:
            # No comparison for first version - return no flags
            return {
                'timing_delays_increase_significant': False,
                'eval_function_introduced': False,
                'eval_function_increase_significant': False,
                'shell_commands_increase_significant': False,
                'size_bytes_increase_significant': False,
                'preinstall_scripts_introduced': False,
                'preinstall_scripts_change': False,
            }
        else:
            # Existing tag
            prev_timing = prev_tag_metrics.get('timing_delays_count')
            curr_timing = curr_tag_metrics.get('timing_delays_count')
            timing_delays_increase = curr_timing - prev_timing

            prev_eval = prev_tag_metrics.get('eval_count')
            curr_eval = curr_tag_metrics.get('eval_count')
            eval_increase = curr_eval - prev_eval

            prev_shell = prev_tag_metrics.get('shell_commands_count')
            curr_shell = curr_tag_metrics.get('shell_commands_count')
            shell_increase = curr_shell - prev_shell

            prev_size_bytes = prev_tag_metrics.get('file_size_bytes')
            curr_size_bytes = curr_tag_metrics.get('file_size_bytes')

            prev_preinstall = prev_tag_metrics.get('list_preinstall_scripts')
            curr_preinstall = curr_tag_metrics.get('list_preinstall_scripts')

            return {
                'timing_delays_increase_significant': timing_delays_increase >= 5 and timing_delays_increase > prev_timing * 0.5,
                'eval_function_introduced': prev_eval == 0 and curr_eval > 0,
                'eval_function_increase_significant': eval_increase >= 5 and eval_increase > prev_eval * 0.5 and prev_eval != 0,
                'shell_commands_increase_significant': shell_increase >= 5 and shell_increase > prev_shell * 0.5,
                'size_bytes_increase_significant': curr_size_bytes > prev_size_bytes * 10,
                'preinstall_scripts_introduced': not prev_preinstall and curr_preinstall,
                'preinstall_scripts_change': prev_preinstall != curr_preinstall and prev_preinstall,
            }