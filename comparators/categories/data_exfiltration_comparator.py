from typing import Dict
from models import VersionMetrics, AggregateVersionMetrics

class DataExfiltrationComparator:
    """Compare data exfiltration & command and control metrics between versions (tags) to identify flags"""
    
    def compare(self, prev_tag_metrics: VersionMetrics, curr_tag_metrics: VersionMetrics, all_prev_tag_metrics: AggregateVersionMetrics) -> Dict:

        if prev_tag_metrics.version == "":
            # No comparison for first version - return no flags
            return {
                'scan_functions_increase_significant': False,
                'sensitive_elements_increase_significant': False,
                'data_transmission_increase': False,
            }
        else:
            prev_scan = prev_tag_metrics.scan_functions_count
            curr_scan = curr_tag_metrics.scan_functions_count
            scan_increase = curr_scan - prev_scan

            prev_sens = prev_tag_metrics.sensitive_elements_count
            curr_sens = curr_tag_metrics.sensitive_elements_count
            sens_increase = curr_sens - prev_sens

            prev_data = prev_tag_metrics.data_transmission_count
            curr_data = curr_tag_metrics.data_transmission_count
            data_increase = curr_data - prev_data

            return {
                'scan_functions_increase_significant': scan_increase >= 5 and scan_increase > prev_scan * 0.5,
                'sensitive_elements_increase_significant': sens_increase >= 50 and sens_increase > prev_sens,
                'data_transmission_increase':  data_increase >= 5 and data_increase > prev_data * 0.5,
            }