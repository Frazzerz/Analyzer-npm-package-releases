from models import Flags, VersionMetrics, AggregateVersionMetrics
from utils.logging_utils import synchronized_print
from .categories import GenericComparator, EvasionComparator, PayloadComparator, DataExfiltrationComparator, CryptojackingComparator, AccountComparator

class VersionComparator:
    """Coordinate version comparison across all categories"""
    
    def __init__(self):
        self.generic_comparator = GenericComparator()
        self.evasion_comparator = EvasionComparator()
        self.payload_comparator = PayloadComparator()
        self.data_exfiltration_comparator = DataExfiltrationComparator()
        self.cryptojacking_comparator = CryptojackingComparator()
        self.account_comparator = AccountComparator()

    def compare_tags(self, all_prev_tag_metrics: AggregateVersionMetrics, prev_tag_metrics: VersionMetrics, curr_tag_metrics: VersionMetrics, package: str, version_from: str, version_to: str) -> Flags:
        """Compare tags (versions) with the aim to identify flags across all categories"""

        flags_dict = {}
        flags_dict.update(self.generic_comparator.compare(prev_tag_metrics, curr_tag_metrics, all_prev_tag_metrics))
        flags_dict.update(self.evasion_comparator.compare(prev_tag_metrics, curr_tag_metrics, all_prev_tag_metrics))
        flags_dict.update(self.payload_comparator.compare(prev_tag_metrics, curr_tag_metrics, all_prev_tag_metrics))
        flags_dict.update(self.data_exfiltration_comparator.compare(prev_tag_metrics, curr_tag_metrics, all_prev_tag_metrics))
        flags_dict.update(self.cryptojacking_comparator.compare(prev_tag_metrics, curr_tag_metrics, all_prev_tag_metrics))
        flags_dict.update(self.account_comparator.compare(prev_tag_metrics, curr_tag_metrics, all_prev_tag_metrics))
        
        flags = Flags(
            package=package,
            version_from=version_from,
            version_to=version_to,
            **flags_dict
        )
        
        return flags