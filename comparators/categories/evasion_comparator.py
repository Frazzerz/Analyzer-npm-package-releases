from typing import Dict
from models import FileMetrics

class EvasionComparator:
    """Compare evasion techniques metrics to identify red flags"""
    
    def compare(self, prev: FileMetrics, curr: FileMetrics) -> Dict:
        
        # New file
        if prev is None:
            return {
                'transformed_code_introduceduced': curr.is_transformed,
                'transformed_code_class_changed': False,
                'inserting_new_code_transformed_differently': False,
                'hex_suspicious_patterns_increase_significant': curr.suspicious_patterns_count > 20,  # threshold
                'timing_delays_introduced': False,
                'dynamic_imports_introduced': False,
                'env_detection_introduced': False,
                'platform_detection_introduced': False,
                'time_detection_introduced': False,

            }
        else:
            # Existing file
            return {
                'transformed_code_introduceduced': not prev.is_transformed and curr.is_transformed,
                'transformed_code_class_changed': prev.transformed_type != curr.transformed_type and prev.is_transformed,
                'inserting_new_code_transformed_differently':  prev.transformed_type != curr.new_code_transformed_type
                                                               and curr.new_code_transformed_type != "none",
                # threshold, increase by at least 100% (double) and at least the increase must be 20
                'hex_suspicious_patterns_increase_significant': (
                    (increase := curr.suspicious_patterns_count - prev.suspicious_patterns_count) >= 20 and 
                    increase > prev.suspicious_patterns_count ),
                'timing_delays_introduced': False,
                'dynamic_imports_introduced': False,
                'env_detection_introduced': False,
                'platform_detection_introduced': False,
                'time_detection_introduced': False,
            }