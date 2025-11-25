from typing import Dict
from models import FileMetrics

class AccountComparator:
    """Compare account compromise metrics to identify red flags"""
    
    def compare(self, prev: FileMetrics, curr: FileMetrics) -> Dict:
        
        # New file
        if prev is None:
            return {
                'npm_new_maintainer': False,
                'npm_awakening_inactive_maintainer': False,
                'npm_new_maintainer_published_first_time_releases': False,
                'npm_ownership_change': False,
                'github_new_contributors': False,
                'github_awakening_inactive_contributors': False,
                'github_new_contributors_published_first_time_releases': False,
                'github_ownership_change': False
            }
        else:
            # Existing file
            return {
                'npm_new_maintainer': curr.npm_maintainers - prev.npm_maintainers > 0,
                'npm_awakening_inactive_maintainer': False,                                                     #TODO
                'npm_new_maintainer_published_first_time_releases': False,                                      #TODO
                'npm_ownership_change': False,                                                                  #TODO
                'github_new_contributors': curr.github_contributors - prev.github_contributors > 0,
                'github_awakening_inactive_contributors': False,                                                #TODO
                'github_new_contributors_published_first_time_releases': False,                                 #TODO
                'github_ownership_change': False                                                                #TODO
            }