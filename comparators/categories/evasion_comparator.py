from typing import Dict, Optional

class EvasionComparator:
    """Compare evasion techniques metrics between two versions (tags) to identify red flags"""
    
    def compare(self, prev_tag_metrics: Optional[Dict], curr_tag_metrics: Dict) -> Dict:
        
        if prev_tag_metrics is None:
            # No comparison for first version - return no flags
            return {
                'obfuscated_code_introduced': False,
                'minified_code_introduced': False,
                'hex_suspicious_patterns_increase_significant': False,
                'platform_detections_increase_significant': False,
            }
        else:
            
            prev_code_type = prev_tag_metrics.get('code_type')
            curr_code_type = curr_tag_metrics.get('code_type')

            prev_suspicious = prev_tag_metrics.get('suspicious_patterns_count')
            curr_suspicious = curr_tag_metrics.get('suspicious_patterns_count')
            suspicious_increase = curr_suspicious - prev_suspicious
            
            prev_platform = prev_tag_metrics.get('platform_detections_count')
            curr_platform = curr_tag_metrics.get('platform_detections_count')
            platform_increase = curr_platform - prev_platform

            return {
                'obfuscated_code_introduced': 'Obfuscated' in curr_code_type and 'Obfuscated' not in prev_code_type,
                'minified_code_introduced': 'Minified' in curr_code_type and 'Minified' not in prev_code_type,
                'hex_suspicious_patterns_increase_significant': suspicious_increase >= 20 and suspicious_increase > prev_suspicious,
                'platform_detections_increase_significant': platform_increase >= 10 and platform_increase > prev_platform,
            }