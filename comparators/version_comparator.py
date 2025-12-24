from typing import List, Dict

from models import *
from utils.logging_utils import synchronized_print
from .categories import *

class VersionComparator:
    """Coordinate version comparison across all categories"""
    
    def __init__(self):
        self.evasion_comparator = EvasionComparator()
        self.payload_comparator = PayloadComparator()
        self.data_exfiltration_comparator = DataExfiltrationComparator()
        self.cryptojacking_comparator = CryptojackingComparator()
        self.account_comparator = AccountComparator()

    def compare_tags(self, all_prev_tag_metrics: Dict, prev_tag_metrics: Dict, curr_tag_metrics: Dict, package: str, version_from: str, version_to: str) -> RedFlag:
        """Compare two tags (versions) and return red flags"""

        red_flags = {}
        red_flags.update(self.evasion_comparator.compare(prev_tag_metrics, curr_tag_metrics))
        red_flags.update(self.payload_comparator.compare(prev_tag_metrics, curr_tag_metrics))
        red_flags.update(self.data_exfiltration_comparator.compare(prev_tag_metrics, curr_tag_metrics))
        red_flags.update(self.cryptojacking_comparator.compare(prev_tag_metrics, curr_tag_metrics))
        red_flags.update(self.account_comparator.compare(prev_tag_metrics, curr_tag_metrics))
        
        change = RedFlag(
            package=package,
            version_from=version_from,
            version_to=version_to,
            **red_flags
        )
        
        return change