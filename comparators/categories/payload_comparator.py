from typing import Dict
from models import FileMetrics

class PayloadComparator:
    """Compare payload delivery & execution metrics to identify red flags"""
    
    def compare(self, prev: FileMetrics, curr: FileMetrics) -> Dict:
        # New file
        if prev is None:
            return {
                'timing_delays_presence_significant': curr.timing_delays_count > 5,         # threshold
                'timing_delays_increase_significant': False,
                'eval_function_presence_significant': curr.eval_count > 5,                  # threshold
                'eval_function_increase_significant': False,
                'shell_commands_presence_significant': curr.shell_commands_count > 5,       # threshold
                'shell_commands_increase_significant': False,
                'size_increase_significant': False,
                'preinstall_scripts_introduced': curr.preinstall_scripts_count > 0,
                'preinstall_scripts_increase': False,
                'suspicious_dependency_introduced': False,
            }
        else:
            # Existing file
            return {
                'timing_delays_presence_significant': False,
                # threshold, increase by at least more than 50% and at least the increase must be 5
                'timing_delays_increase_significant': ((increase := curr.timing_delays_count - prev.timing_delays_count) >= 5 
                                                       and increase > prev.timing_delays_count * 0.5 ),
                'eval_function_presence_significant': False,
                'eval_function_increase_significant': (increase := curr.eval_count - prev.eval_count) >= 5 and increase > prev.eval_count * 0.5,
                'shell_commands_presence_significant': False,
                'shell_commands_increase_significant': ((increase := curr.shell_commands_count - prev.shell_commands_count) >= 5 
                                                       and increase > prev.shell_commands_count * 0.5 ),
                'size_increase_significant': curr.file_size_bytes > prev.file_size_bytes * 2,                                 # 100% increase
                'preinstall_scripts_introduced': prev.preinstall_scripts_count == 0 and curr.preinstall_scripts_count > 0,
                'preinstall_scripts_increase': curr.preinstall_scripts_count > prev.preinstall_scripts_count and prev.preinstall_scripts_count != 0,
                'suspicious_dependency_introduced': False,
            }