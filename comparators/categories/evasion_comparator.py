from typing import Dict
from models import VersionMetrics, AggregateVersionMetrics

class EvasionComparator:
    """Compare evasion techniques metrics between versions (tags) to identify flags"""
    
    def compare(self, prev_tag_metrics: VersionMetrics, curr_tag_metrics: VersionMetrics, all_prev_tag_metrics: AggregateVersionMetrics) -> Dict:
        
        if prev_tag_metrics.version == "":
            # No comparison for first version - return no flags
            return {
                'obfuscated_code_introduced': False,
                'minified_code_introduced': False,
                'hex_obfuscation_patterns_increase_significant': False,
                'platform_detections_increase_significant': False,
            }
        else:
            
            prev_code_types = prev_tag_metrics.code_types
            curr_code_types = curr_tag_metrics.code_types

            prev_obfuscation = prev_tag_metrics.obfuscation_patterns_count
            curr_obfuscation = curr_tag_metrics.obfuscation_patterns_count
            obfuscation_increase = curr_obfuscation - prev_obfuscation
            
            prev_platform = prev_tag_metrics.platform_detections_count
            curr_platform = curr_tag_metrics.platform_detections_count
            platform_increase = curr_platform - prev_platform

            return {
                'obfuscated_code_introduced': 'Obfuscated' in curr_code_types and 'Obfuscated' not in prev_code_types,
                'minified_code_introduced': 'Minified' in curr_code_types and 'Minified' not in prev_code_types,
                'hex_obfuscation_patterns_increase_significant': obfuscation_increase >= 20 and obfuscation_increase > prev_obfuscation,
                'platform_detections_increase_significant': platform_increase >= 10 and platform_increase > prev_platform,
            }