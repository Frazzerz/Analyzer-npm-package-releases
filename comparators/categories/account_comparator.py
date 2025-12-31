from typing import Dict
from datetime import datetime, timedelta, timezone
from models import VersionMetrics, AggregateVersionMetrics
class AccountComparator:
    """Compare account compromise & release integrity anomalies metrics between versions (tags) to identify flags"""
    
    def compare(self, prev_tag_metrics: VersionMetrics, curr_tag_metrics: VersionMetrics, all_prev_tag_metrics: AggregateVersionMetrics) -> Dict:
        
        UTC_MIN_DATETIME = datetime.min.replace(tzinfo=timezone.utc)

        if prev_tag_metrics.version == "":
            # No comparison for first version - return no flags
            return {
                #'npm_new_maintainer': False,
                #'npm_awakening_inactive_maintainer': False,
                #'npm_new_maintainer_published_first_time_releases': False,
                #'github_new_contributors': False,
                'hash_mismatch_commit_between_npm_and_github': False,
                #'npm_before_github': curr.npm_release_date < curr.github_release_date,      # test
                #'anomalous_time': False,
                'package_reactivation': False
            }
        else:
            prev_npm_date = prev_tag_metrics.npm_release_date
            if prev_npm_date is None or prev_npm_date == "":
                prev_npm_date = UTC_MIN_DATETIME
            elif isinstance(prev_npm_date, str):
                prev_npm_date = datetime.fromisoformat(prev_npm_date)

            curr_npm_date = curr_tag_metrics.npm_release_date
            if curr_npm_date is None or curr_npm_date == "":
                curr_npm_date = UTC_MIN_DATETIME
            elif isinstance(curr_npm_date, str):
                curr_npm_date = datetime.fromisoformat(curr_npm_date)
            
            curr_npm_hash_commit = curr_tag_metrics.npm_hash_commit
            if curr_npm_hash_commit is None:
                curr_npm_hash_commit = ""
            curr_github_hash_commit = curr_tag_metrics.github_hash_commit
            if curr_github_hash_commit is None:
                curr_github_hash_commit = ""
            
            return {
                #'npm_new_maintainer': curr.npm_maintainers - prev.npm_maintainers > 0,   #It makes too much noise  
                #'npm_awakening_inactive_maintainer': False,
                #'npm_new_maintainer_published_first_time_releases': False,
                #'github_new_contributors': curr.github_contributors - prev.github_contributors > 0,  #It makes too much noise
                'hash_mismatch_commit_between_npm_and_github': (
                    curr_npm_hash_commit != curr_github_hash_commit and curr_npm_hash_commit != "" and curr_github_hash_commit != ""
                ),
                #'npm_before_github': curr.npm_release_date < curr.github_release_date,      # test
                #'anomalous_time': False,
                'package_reactivation': (curr_npm_date - prev_npm_date) > timedelta(days=365*2) and prev_npm_date != UTC_MIN_DATETIME
            }