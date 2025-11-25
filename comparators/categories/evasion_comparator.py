from typing import Dict
from models import FileMetrics

class EvasionComparator:
    """Compare evasion techniques metrics to identify red flags"""
    
    def compare(self, prev: FileMetrics, curr: FileMetrics) -> Dict:
        
        # New file
        if prev is None:
            return {
                'obfuscation_introduced': curr.is_obfuscated,                                                                   # TODO ALL, placeholder
                'obfuscation_class_changed': False,
                'new_code_obfuscated_differently': curr.is_obfuscated,
                'timing_delays_introduced': curr.timing_delays > 0,
                'dynamic_imports_introduced': curr.dynamic_imports > 0,
                'env_detection_introduced': curr.env_node_env > 0,
                'platform_detection_introduced': curr.env_platform > 0,
                'time_detection_introduced': curr.execution_time > 0,

            }
        else:
            # Existing file
            return {
                'obfuscation_introduced': (not prev.is_obfuscated and curr.is_obfuscated),                                      # TODO ALL, placeholder
                'obfuscation_class_changed': (prev.obfuscation_type != curr.obfuscation_type and curr.is_obfuscated),
                'new_code_obfuscated_differently': (prev.obfuscation_type == "none" and curr.obfuscation_type != "none"),
                'timing_delays_introduced': (prev.timing_delays == 0 and curr.timing_delays > 0), # se aumenta rispetto a prima, anche per ultimi 3
                'dynamic_imports_introduced': (prev.dynamic_imports == 0 and curr.dynamic_imports > 0),
                'env_detection_introduced': (prev.env_node_env == 0 and curr.env_node_env > 0),
                'platform_detection_introduced': (prev.env_platform == 0 and curr.env_platform > 0),
                'time_detection_introduced': (prev.execution_time == 0 and curr.execution_time > 0),
            }