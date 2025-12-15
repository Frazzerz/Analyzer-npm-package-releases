from typing import Dict, Optional
from datetime import datetime, timedelta, timezone

class AccountComparator:
    """Compare account compromise & release integrity anomalies metrics between two versions (tags) to identify red flags"""
    
    def compare(self, prev_tag_metrics: Optional[Dict], curr_tag_metrics: Dict) -> Dict:
        
        UTC_MIN_DATETIME = datetime.min.replace(tzinfo=timezone.utc)

        if prev_tag_metrics is None:
            # No comparison for first version - return no flags
            return {
                #'npm_new_maintainer': False,
                #'npm_awakening_inactive_maintainer': False,
                #'npm_new_maintainer_published_first_time_releases': False,
                #'github_new_contributors': False,
                #'github_publisher_release': False,
                #'github_repository_owner': False,
                'hash_mismatch_commit_between_npm_and_github': False,
                #'npm_before_github': curr.npm_release_date < curr.github_release_date,      # test
                #'hash_mismatch_file_between_npm_and_github': False,
                #'anomalous_time': False,
                'package_reactivation': False,
                #'dependency_issues_keywords': False
            }
        else:
            prev_npm_date = prev_tag_metrics.get('npm_release_date')
            if prev_npm_date is None:
                prev_npm_date = UTC_MIN_DATETIME
            elif isinstance(prev_npm_date, str):
                prev_npm_date = datetime.fromisoformat(prev_npm_date)

            curr_npm_date = curr_tag_metrics.get('npm_release_date')
            if curr_npm_date is None:
                curr_npm_date = UTC_MIN_DATETIME
            elif isinstance(curr_npm_date, str):
                curr_npm_date = datetime.fromisoformat(curr_npm_date)

            return {
                #'npm_new_maintainer': curr.npm_maintainers - prev.npm_maintainers > 0,   #It makes too much noise  
                #'npm_awakening_inactive_maintainer': False,
                #'npm_new_maintainer_published_first_time_releases': False,
                #'github_new_contributors': curr.github_contributors - prev.github_contributors > 0,  #It makes too much noise  
                #'github_publisher_release': False,
                #'github_repository_owner': False,
                'hash_mismatch_commit_between_npm_and_github': (
                    curr_tag_metrics.get('npm_hash_commit') != curr_tag_metrics.get('github_hash_commit') and 
                    curr_tag_metrics.get('github_hash_commit') != "" and 
                    curr_tag_metrics.get('npm_hash_commit') != ""
                ),
                #'npm_before_github': curr.npm_release_date < curr.github_release_date,      # test
                #'hash_mismatch_file_between_npm_and_github': False,
                #'anomalous_time': False,
                'package_reactivation': (curr_npm_date - prev_npm_date) > timedelta(days=365*2) and prev_npm_date != UTC_MIN_DATETIME,
                #'dependency_issues_keywords': False
            }

'''
    def compare(self, prev: FileMetrics, curr: FileMetrics) -> Dict:
        
        UTC_MIN_DATETIME = datetime.min.replace(tzinfo=timezone.utc)

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
                'package_reactivation': (curr.npm_release_date - prev.npm_release_date) > timedelta(days=365*2) and prev.npm_release_date != UTC_MIN_DATETIME,    # More than 2 years gap
                #'dependency_issues_keywords': False
            }
'''