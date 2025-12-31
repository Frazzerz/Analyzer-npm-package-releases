from typing import Dict
from models import VersionMetrics, AggregateVersionMetrics

class GenericComparator:
    """Compare generic metrics between versions (tags) to identify flags"""
        
    def compare(self, prev_tag_metrics: VersionMetrics, curr_tag_metrics: VersionMetrics, all_prev_tag_metrics: AggregateVersionMetrics) -> Dict:
            
            if prev_tag_metrics.version == "":
                # No comparison for first version - return no flags
                return {
                    'size_bytes_increase_significant': False,
                }
            else:
                # Existing tag

                prev_size_bytes = prev_tag_metrics.total_size_bytes
                curr_size_bytes = curr_tag_metrics.total_size_bytes

                return {
                    'size_bytes_increase_significant': curr_size_bytes > prev_size_bytes * 10,
                }