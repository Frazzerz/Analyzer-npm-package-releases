from typing import Dict, Optional

class EvasionComparator:
    """Compare evasion techniques metrics between two versions (tags) to identify red flags"""
    
    def compare(self, prev_tag_metrics: Optional[Dict], curr_tag_metrics: Dict) -> Dict:
        
        if prev_tag_metrics is None:
            # No comparison for first version - return no flags
            return {
                'obfuscated_code_introduced': False,
                'minified_code_introduced': False,
                'hex_obfuscation_patterns_increase_significant': False,
                'platform_detections_increase_significant': False,
            }
        else:
            
            prev_code_types = prev_tag_metrics.get('code_types')
            curr_code_types = curr_tag_metrics.get('code_types')

            prev_obfuscation = prev_tag_metrics.get('obfuscation_patterns_count')
            curr_obfuscation = curr_tag_metrics.get('obfuscation_patterns_count')
            obfuscation_increase = curr_obfuscation - prev_obfuscation
            
            prev_platform = prev_tag_metrics.get('platform_detections_count')
            curr_platform = curr_tag_metrics.get('platform_detections_count')
            platform_increase = curr_platform - prev_platform

            return {
                'obfuscated_code_introduced': 'Obfuscated' in curr_code_types and 'Obfuscated' not in prev_code_types,
                'minified_code_introduced': 'Minified' in curr_code_types and 'Minified' not in prev_code_types,
                'hex_obfuscation_patterns_increase_significant': obfuscation_increase >= 20 and obfuscation_increase > prev_obfuscation,
                'platform_detections_increase_significant': platform_increase >= 10 and platform_increase > prev_platform,
            }