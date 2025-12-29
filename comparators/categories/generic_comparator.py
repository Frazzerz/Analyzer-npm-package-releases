from typing import Dict, Optional

class GenericComparator:
    """Compare generic metrics between versions (tags) to identify red flags"""
        
    def compare(self, prev_tag_metrics: Optional[Dict], curr_tag_metrics: Dict) -> Dict:
            
            if prev_tag_metrics is None:
                # No comparison for first version - return no flags
                return {
                    'size_bytes_increase_significant': False,
                }
            else:
                # Existing tag

                prev_size_bytes = prev_tag_metrics.get('file_size_bytes')
                curr_size_bytes = curr_tag_metrics.get('file_size_bytes')

                return {
                    'size_bytes_increase_significant': curr_size_bytes > prev_size_bytes * 10,
                    }