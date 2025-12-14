from typing import List

from models import *
from .categories import *

class VersionComparator:
    """Coordinate version comparison across all categories"""
    
    def __init__(self):
        self.evasion_comparator = EvasionComparator()
        self.payload_comparator = PayloadComparator()
        self.data_exfiltration_comparator = DataExfiltrationComparator()
        self.cryptojacking_comparator = CryptojackingComparator()
        self.account_comparator = AccountComparator()
    
    def compare_versions(self, prev_metrics: List[FileMetrics], curr_metrics: List[FileMetrics]) -> List[RedFlagChanges]:
        """Compare two versions and return red flags"""
        changes = []
        
        prev_map = {m.file_path: m for m in prev_metrics}
        curr_map = {m.file_path: m for m in curr_metrics}
        
        for file_path in curr_map.keys():
            prev = prev_map.get(file_path)
            curr = curr_map[file_path]
            
            # Collect red flags from all categories
            red_flags = {}
            red_flags.update(self.evasion_comparator.compare(prev, curr))
            red_flags.update(self.payload_comparator.compare(prev, curr))
            red_flags.update(self.data_exfiltration_comparator.compare(prev, curr))
            red_flags.update(self.cryptojacking_comparator.compare(prev, curr))
            red_flags.update(self.account_comparator.compare(prev, curr))
            
            change = RedFlagChanges(
                package=curr.package,
                file_path=curr.file_path,
                version_from=prev.version if prev else "new_file",
                version_to=curr.version,
                **red_flags
            )
            changes.append(change)
        
        return changes