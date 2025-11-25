from typing import Dict
from models import FileMetrics

class PayloadComparator:
    """Compare payload delivery & execution metrics to identify red flags"""
    
    def compare(self, prev: FileMetrics, curr: FileMetrics) -> Dict:
        
        # New file
        if prev is None:
            return {
                'eval_shell_introduced': (curr.eval > 0 or curr.shell_commands > 0),                                                        # TODO, placeholder
                'new_files_added_inside_pkg': False,                                                                                        # TODO, placeholder
                'size_increase_significant': False,
                'dependency_suspicious_pkg_added_few_downloads': False,                                                                     # TODO, placeholder
                'dependency_suspicious_pkg_added_just_created': False,                                                                      # TODO, placeholder
                'dependency_suspicious_pkg_added_typesquatted': False,                                                                      # TODO, placeholder
            }
        else:
            # Existing file
            return {
                'eval_shell_introduced': ((prev.eval == 0 and curr.eval > 0) or(prev.shell_commands == 0 and curr.shell_commands > 0)),     # TODO, placeholder
                'new_files_added_inside_pkg': False,                                                                                        # TODO, placeholder
                'size_increase_significant': (curr.file_size_bytes > prev.file_size_bytes * 2),         # 100% increase
                'dependency_suspicious_pkg_added_few_downloads': False,                                                                     # TODO, placeholder
                'dependency_suspicious_pkg_added_just_created': False,                                                                      # TODO, placeholder
                'dependency_suspicious_pkg_added_typesquatted': False,                                                                      # TODO, placeholder
            }