from typing import Dict, Optional

class EvasionComparator:
    """Compare evasion techniques metrics between two versions (tags) to identify red flags"""
    
    def compare(self, prev_tag_metrics: Optional[Dict], curr_tag_metrics: Dict) -> Dict:
        
        if prev_tag_metrics is None:
            # No comparison for first version - return no flags
            return {
                'transformed_code_introduced': False,
                'transformed_code_class_changed': False,
                'inserting_new_code_transformed_differently': False,
                'hex_suspicious_patterns_presence_significant': False,
                'hex_suspicious_patterns_increase_significant': False,
                'platform_detections_presence_significant': False,
                'platform_detections_increase_significant': False,
            }
        else:

            prev_suspicious = prev_tag_metrics.get('suspicious_patterns_count')
            curr_suspicious = curr_tag_metrics.get('suspicious_patterns_count')
            suspicious_increase = curr_suspicious - prev_suspicious
            
            prev_platform = prev_tag_metrics.get('platform_detections_count')
            curr_platform = curr_tag_metrics.get('platform_detections_count')
            platform_increase = curr_platform - prev_platform

            return {
                'transformed_code_introduced': False,
                'transformed_code_class_changed': False,
                'inserting_new_code_transformed_differently': False,
                'hex_suspicious_patterns_presence_significant': False,
                'hex_suspicious_patterns_increase_significant': (
                    suspicious_increase >= 20 and 
                    suspicious_increase > prev_suspicious
                ),
                'platform_detections_presence_significant': False,
                'platform_detections_increase_significant': (
                    platform_increase >= 10 and 
                    platform_increase > prev_platform
                ),
                #'presence_of_concatenated_elements': False,
            }
    
'''
    def compare(self, prev: FileMetrics, curr: FileMetrics) -> Dict:
        # New file
        if prev is None:
            return {
                'transformed_code_introduced': curr.is_transformed,
                'transformed_code_class_changed': False,
                'inserting_new_code_transformed_differently': False,
                'hex_suspicious_patterns_presence_significant': curr.suspicious_patterns_count > 20,    # threshold
                'hex_suspicious_patterns_increase_significant': False,
                'platform_detections_presence_significant': curr.platform_detections_count > 10,        # threshold
                'platform_detections_increase_significant': False,
                #'presence_of_concatenated_elements': False,
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
                    (increase := curr.platform_detections_count - prev.platform_detections_count) >= 10 and 
                    increase > prev.platform_detections_count ),
                #'presence_of_concatenated_elements': False,
            }
'''