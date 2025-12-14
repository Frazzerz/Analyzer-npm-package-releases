from typing import Dict
from models import FileMetrics
from datetime import timedelta

class AccountComparator:
    """Compare account compromise & release integrity anomalies metrics to identify red flags"""
    
    def compare(self, prev: FileMetrics, curr: FileMetrics) -> Dict:
        
        # New file
        if prev is None:
            return {
                #'npm_new_maintainer': False,
                #'npm_awakening_inactive_maintainer': False,
                #'npm_new_maintainer_published_first_time_releases': False,
                #'github_new_contributors': False,
                #'github_publisher_release': False,
                #'github_repository_owner': False,
                'hash_mismatch_commit_between_npm_and_github': curr.npm_hash_commit != curr.github_hash_commit and curr.github_hash_commit != "" and curr.npm_hash_commit != "",
                #'npm_before_github': curr.npm_release_date < curr.github_release_date,      # test
                #'hash_mismatch_file_between_npm_and_github': False,
                #'anomalous_time': False,
                'package_reactivation': False,
                #'dependency_issues_keywords': False
            }
        else:
            # Existing file
            return {
                #'npm_new_maintainer': curr.npm_maintainers - prev.npm_maintainers > 0,   #It makes too much noise  
                #'npm_awakening_inactive_maintainer': False,
                #'npm_new_maintainer_published_first_time_releases': False,
                #'github_new_contributors': curr.github_contributors - prev.github_contributors > 0,  #It makes too much noise  
                #'github_publisher_release': False,
                #'github_repository_owner': False,
                'hash_mismatch_commit_between_npm_and_github': curr.npm_hash_commit != curr.github_hash_commit and curr.github_hash_commit != "" and curr.npm_hash_commit != "",
                #'npm_before_github': curr.npm_release_date < curr.github_release_date,      # test
                #'hash_mismatch_file_between_npm_and_github': False,
                #'anomalous_time': False,
                'package_reactivation': (curr.npm_release_date - prev.npm_release_date) > timedelta(days=365*2),    # More than 2 years gap
                #'dependency_issues_keywords': False
            }