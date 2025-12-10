from typing import Dict
from models import FileMetrics

class EvasionComparator:
    """Compare evasion techniques metrics to identify red flags"""
    
    def compare(self, prev: FileMetrics, curr: FileMetrics) -> Dict:
        # New file
        if prev is None:
            return {
                'transformed_code_introduced': curr.is_transformed,
                'transformed_code_class_changed': False,
                'inserting_new_code_transformed_differently': False,
                'hex_suspicious_patterns_presence_significant': curr.suspicious_patterns_count > 20,    # threshold
                'hex_suspicious_patterns_increase_significant': False,
                'platform_detections_presence_significant': curr.platform_detections_count > 20,        # threshold
                'platform_detections_increase_significant': False,
                'presence_of_concatenated_elements': False,
            }
        else:
            # Existing file
            return {
                'transformed_code_introduced': not prev.is_transformed and curr.is_transformed,
                'transformed_code_class_changed': prev.transformed_type != curr.transformed_type and prev.is_transformed,
                'inserting_new_code_transformed_differently':  prev.transformed_type != curr.new_code_transformed_type
                                                               and curr.new_code_transformed_type != "none",
                'hex_suspicious_patterns_presence_significant': False,
                # threshold, increase by at least more than 100% (double) and at least the increase must be 20
                'hex_suspicious_patterns_increase_significant': (
                    (increase := curr.suspicious_patterns_count - prev.suspicious_patterns_count) >= 20 and 
                    increase > prev.suspicious_patterns_count ),
                'platform_detections_presence_significant': False,
                'platform_detections_increase_significant': (
                    (increase := curr.platform_detections_count - prev.platform_detections_count) >= 20 and 
                    increase > prev.platform_detections_count ),
                'presence_of_concatenated_elements': False,
            }