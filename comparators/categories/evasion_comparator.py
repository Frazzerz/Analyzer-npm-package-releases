from typing import Dict
from models import FileMetrics

class EvasionComparator:
    """Compare evasion techniques metrics to identify red flags"""
    
    def compare(self, prev: FileMetrics, curr: FileMetrics) -> Dict:
        
        # New file
        if prev is None:
            return {        # TODO ALL, placeholder
                'obfuscation_introduced': curr.transformed_type == "obfuscated",
                'obfuscation_class_changed': False,
                'new_code_obfuscated_differently': False,
                'hex_suspicious_patterns_increase_significant': curr.suspicious_patterns_count > 20,  # threshold
                'timing_delays_introduced': False,
                'dynamic_imports_introduced': False,
                'env_detection_introduced': False,
                'platform_detection_introduced': False,
                'time_detection_introduced': False,

            }
        else:
            # Existing file
            return {        # TODO ALL, placeholder
                'obfuscation_introduced': prev.transformed_type != "obfuscated" and curr.transformed_type == "obfuscated",
                'obfuscation_class_changed': False, #prev.transformed_type != curr.transformed_type, # per ora non distiguo i tipi di offuscamento
                'new_code_obfuscated_differently': False,
                'hex_suspicious_patterns_increase_significant': curr.suspicious_patterns_count - prev.suspicious_patterns_count > 20,  # threshold
                'timing_delays_introduced': False,                      # se aumenta rispetto a prima, anche per ultimi 3
                'dynamic_imports_introduced': False,
                'env_detection_introduced': False,
                'platform_detection_introduced': False,
                'time_detection_introduced': False,
            }