from typing import Dict
from models import FileMetrics
from datetime import timedelta

class ReleaseComparator:
    """Compare release integrity anomalies metrics to identify red flags"""
    
    def compare(self, prev: FileMetrics, curr: FileMetrics) -> Dict:
        
        # New file
        if prev is None:
            return {
                'npm_before_github': curr.npm_release_date < curr.github_release_date,
                'hash_mismatch_between_npm_and_github': curr.hash_npm != curr.hash_github,
                'anomalous_time': False,
                'package_reactivation': False,
                'dependency_issues_keywords': False                                                                           # TODO
            }
        else:
            # Existing file
            return {
                'npm_before_github': curr.npm_release_date < curr.github_release_date,
                'hash_mismatch_between_npm_and_github': curr.hash_npm != curr.hash_github,
                'anomalous_time': False,                                                                                      # TODO, da pensarci
                'package_reactivation': (curr.npm_release_date - prev.npm_release_date) > timedelta(days=365*2),    # More than 2 years gap
                'dependency_issues_keywords': False                                                                           # TODO
            }