from typing import Dict
from git import Repo
from utils import NPMClient
from typing import Optional
from datetime import datetime, timezone
class AccountAnalyzer:
    """Analyzes account compromise & release integrity anomalies"""
    
    def __init__(self):
        self.npm_client = NPMClient()
        self._package_cache = {}
    
    def analyze(self, package_info: Dict) -> Dict:

        metrics = {
            'npm_maintainers': 0,
            'npm_maintainers_nicks': [],
            'npm_maintainers_emails': [],
            'npm_maintainer_published_release': '',
            #'github_contributors': 0,
            #'github_contributors_nicks': [],
            #'github_contributors_emails': [],            
            #'github_publisher_release': '',    # Placeholder
            #'github_repository_owner': '',     # Placeholder
            'npm_hash_commit': '',
            'github_hash_commit': '',
            #'npm_hash_file': '',               # Placeholder
            #'github_hash_file': '',            # Placeholder
            'npm_release_date': datetime.min,       # missing date
            #'github_release_date': datetime.min,    # missing date
            #'malicious_issues': 0              # Placeholder
        }
        
        #return metrics

        # For local versions or deobfuscated versions
        if not package_info or package_info.get('info') == "local" or  package_info.get('info') == "deobfuscated":
            return metrics
        
        package_name = package_info.get('name', '')
        version = package_info.get('version', '')
        git_repo_path = package_info.get('git_repo_path')
        
        # If the package is NOT cached, fetch it from NPM
        if package_name not in self._package_cache:
            self._package_cache[package_name] = self.npm_client.get_npm_package_data(package_name)
        
        # Use cached data (whether just added or already present)
        npm_data = self._package_cache[package_name]
        if not npm_data:
            return metrics
        
        metrics['npm_maintainers'], metrics['npm_maintainers_nicks'], metrics['npm_maintainers_emails'], metrics['npm_maintainer_published_release'], metrics['npm_hash_commit'], metrics['npm_release_date'] = self._get_npm_metrics(npm_data, version)
        metrics['github_hash_commit'] = self._get_github_metrics(git_repo_path, version)

        return metrics
    
    def _normalize_tag(self, repo: Repo, version: str) -> Optional[str]:
        """Normalize tag name and check if it exists in the repository"""
        tag_name = version
        if f"v{version}" in repo.tags:
            tag_name = f"v{version}"
        elif version not in repo.tags:
            return None
        return tag_name
    
    def _parse_date(self, date_str: str) -> Optional[datetime]:
        """Parse ISO date and convert to UTC+0"""
        if not date_str:
            return None
        try:
            # Handle 'Z' suffix for UTC
            if date_str.endswith("Z"):
                date_str = date_str[:-1] + "+00:00"

            # Parse the ISO format string
            dt = datetime.fromisoformat(date_str)
            
            # If it has no timezone, assume UTC
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)

            # Convert to UTC timezone
            return dt.astimezone(timezone.utc)

        except Exception as e:
            print(f"Error parsing date {date_str}: {e}")
            return None
    
    def _get_npm_metrics(self, npm_data: Dict, version: str) -> tuple[int, list, list, str, str, str]:
        """Returns all NPM metrics:
                number_of_maintainers, maintainers_nicks, maintainers_emails,
                release_publisher, commit_hash, release_time"""
        try:
            # Check if version exists in npm data
            if 'versions' not in npm_data or version not in npm_data['versions']:
                return 0, [], [], '', '', ''    # Empty content
            
            version_data = npm_data['versions'][version]
            
            # Get maintainers/owners
            maintainers = version_data.get('maintainers', [])
            nicks = [maintainer.get('name', '') for maintainer in maintainers if maintainer.get('name')]
            emails = [maintainer.get('email', '') for maintainer in maintainers if maintainer.get('email')]
            
            # Get publisher info
            npm_user = version_data.get('_npmUser', {})
            published_release = npm_user.get('name', '') if npm_user else ''
            
            # Get git commit hash
            npm_hash_commit = version_data.get('gitHead', "")
            
            # Get release time
            release_time = ""
            if 'time' in npm_data and version in npm_data['time']:
                release_time = self._parse_date(npm_data['time'][version])
            
            return len(maintainers), nicks, emails, published_release, npm_hash_commit, release_time
            
        except Exception as e:
            print(f"Error getting NPM metrics: {e}")
            return 0, [], [], '', '', ''        # Empty content

    def _get_github_metrics(self, repo_path: str, version: str) -> str:
        """Returns all GitHub metrics: for now only commit_hash"""
        try:
            if not repo_path:
                return ''  # Empty content
            
            repo = Repo(repo_path)

            # Take the cotributors from the git repository
            #contributors_names = set()
            #contributors_emails = set()            
            #for commit in repo.iter_commits():
            #    if commit.author:
            #        contributors_names.add(commit.author.name)
            #        contributors_emails.add(commit.author.email)
            #return len(contributors_names), list(contributors_names), list(contributors_emails)

            tag_name = self._normalize_tag(repo, version)
            if not tag_name:
                return ''   # Empty content
            
            tag = repo.tags[tag_name]
            #commit = tag.commit
            
            # test github_release_date, take the release time from GitHub repository  -  2021-11-04T17:48:07+07:00
            #release_time = self._parse_date(commit.committed_datetime.isoformat())

            return tag.commit.hexsha
        except Exception as e:
            print(f"Error getting GitHub metrics: {e}")
            return '' # Empty content