from typing import Dict
from models import FileMetrics

class DataExfiltrationComparator:
    """Compare data exfiltration & command and control metrics to identify red flags"""
    
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
                # threshold, increase by at least more than 100% (double) and at least the increase must be 5
                'scan_functions_increase_significant': (( increase := curr.scan_functions_count - prev.scan_functions_count) >= 5 and
                    increase > prev.scan_functions_count * 0.5 ),
                'sensitive_elements_presence_significant': False,
                'sensitive_elements_increase_significant': (( increase := curr.sensitive_elements_count - prev.sensitive_elements_count) >= 50 and
                    increase > prev.sensitive_elements_count ),
                #'data_transmission_introduced': False,
                #'data_transmission_increase': False,
            }