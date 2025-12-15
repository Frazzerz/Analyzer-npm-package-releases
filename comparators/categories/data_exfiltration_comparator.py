from typing import Dict, Optional

class DataExfiltrationComparator:
    """Compare data exfiltration & command and control metrics between two versions (tags) to identify red flags"""
    
    def compare(self, prev_tag_metrics: Optional[Dict], curr_tag_metrics: Dict) -> Dict:

        if prev_tag_metrics is None:
            # No comparison for first version - return no flags
            return {
                'scan_functions_presence_significant': False,
                'scan_functions_increase_significant': False,
                'sensitive_elements_presence_significant': False,
                'sensitive_elements_increase_significant': False,
                #'data_transmission_introduced': False,
                #'data_transmission_increase': False,
            }
        else:
            prev_scan = prev_tag_metrics.get('scan_functions_count')
            curr_scan = curr_tag_metrics.get('scan_functions_count')
            scan_increase = curr_scan - prev_scan

            prev_sens = prev_tag_metrics.get('sensitive_elements_count')
            curr_sens = curr_tag_metrics.get('sensitive_elements_count')
            sens_increase = curr_sens - prev_sens

            return {
                'scan_functions_presence_significant': False,
                'scan_functions_increase_significant': (scan_increase >= 5 and scan_increase > prev_scan * 0.5),
                'sensitive_elements_presence_significant': False,
                'sensitive_elements_increase_significant': (sens_increase >= 50 and sens_increase > prev_sens),
                #'data_transmission_introduced': False,
                #'data_transmission_increase': False,
            }

'''
    def compare(self, prev: FileMetrics, curr: FileMetrics) -> Dict:        
        # New file
        if prev is None:
            return {
                'scan_functions_presence_significant': curr.scan_functions_count > 5,          # threshold
                'scan_functions_increase_significant': False,
                'sensitive_elements_presence_significant': curr.sensitive_elements_count > 50,  # threshold
                'sensitive_elements_increase_significant': False,
                #'data_transmission_introduced': False,
                #'data_transmission_increase': False,
            }
        else:
            # Existing file
            return {
                'scan_functions_presence_significant': False,
                # threshold, increase by at least more than 50% (double) and at least the increase must be 5
                'scan_functions_increase_significant': (( increase := curr.scan_functions_count - prev.scan_functions_count) >= 5 and
                    increase > prev.scan_functions_count * 0.5 ),
                'sensitive_elements_presence_significant': False,
                'sensitive_elements_increase_significant': (( increase := curr.sensitive_elements_count - prev.sensitive_elements_count) >= 50 and
                    increase > prev.sensitive_elements_count ),
                #'data_transmission_introduced': False,
                #'data_transmission_increase': False,
            }
'''