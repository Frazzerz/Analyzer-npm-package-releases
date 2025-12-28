from typing import Dict, Optional
from zipfile import Path
from git import Repo
from utils import NPMClient
from datetime import datetime, timezone
from utils import synchronized_print

class AccountAnalyzer:
    """Analyzes account compromise & release integrity anomalies"""
    _npm_cache: Dict[str, Dict] = {}
    UTC_MIN_DATETIME = datetime.min.replace(tzinfo=timezone.utc)

    def __init__(self, pkg_name: str = ""):
        self.package_name = pkg_name
        self.npm_client = NPMClient(pkg_name=pkg_name)   
    
    def _get_npm_data_cached(self) -> Optional[Dict]:
        """Fetch NPM data with caching"""
        # If it's already cached, it will return immediately.
        if self.package_name in AccountAnalyzer._npm_cache:
            #synchronized_print(f"Using cached NPM data for {self.package_name}")
            return AccountAnalyzer._npm_cache[self.package_name]
        
        # Otherwise, fetch from NPM
        #synchronized_print(f"Fetching NPM data for {self.package_name}")
        npm_data = self.npm_client.get_npm_package_data()
        
        AccountAnalyzer._npm_cache[self.package_name] = npm_data
        return npm_data
    
    def analyze(self, version: str, git_repo_path: Path, source: str) -> Dict:
        metrics = {
            'npm_maintainers': 0,
            'npm_maintainers_nicks': [],
            'npm_maintainers_emails': [],
            'npm_maintainer_published_release': '',
            #'github_contributors': 0,
            #'github_contributors_nicks': [],
            #'github_contributors_emails': [],
            'npm_hash_commit': '',
            'github_hash_commit': '',
            'npm_release_date': AccountAnalyzer.UTC_MIN_DATETIME,        # missing date, empty metrics
            #'github_release_date': AccountAnalyzer.UTC_MIN_DATETIME,    # missing date, empty metrics
        }

        if source in ("local", "deobfuscated"):
            return metrics
        
        # Get npm metrics
        npm_data = self._get_npm_data_cached()
        if npm_data and ('versions' in npm_data or version in npm_data['versions']):
            version_data = npm_data['versions'][version]

            # Get maintainers/owners
            maintainers = version_data.get('maintainers', [])
            metrics['npm_maintainers'] = len(maintainers)

            metrics['npm_maintainers_nicks'] = [maintainer.get('name', '') for maintainer in maintainers if maintainer.get('name')]
            metrics['npm_maintainers_emails'] = [maintainer.get('email', '') for maintainer in maintainers if maintainer.get('email')]
                
            # Get publisher info
            npm_user = version_data.get('_npmUser', {})
            metrics['npm_maintainer_published_release'] = npm_user.get('name', '') if npm_user else ''
            
            # Get git commit hash
            metrics['npm_hash_commit'] = version_data.get('gitHead', "")
            
            # Get release time
            if 'time' in npm_data and version in npm_data['time']:
                metrics['npm_release_date'] = self._parse_date(npm_data['time'][version])
        
        # Get GitHub metrics
        if git_repo_path:    
            repo = Repo(str(git_repo_path))
            '''
            # Take the cotributors from the git repository
            contributors_names = set()
            contributors_emails = set()            
            for commit in repo.iter_commits():
                if commit.author:
                    contributors_names.add(commit.author.name)
                    contributors_emails.add(commit.author.email)
            return len(contributors_names), list(contributors_names), list(contributors_emails)
            '''
            tag_name = self._normalize_tag(repo, version)
            if tag_name:
                tag = repo.tags[tag_name]
                #commit = tag.commit
                # test github_release_date, take the release time from GitHub repository  -  2021-11-04T17:48:07+07:00
                #release_time = self._parse_date(commit.committed_datetime.isoformat())
                metrics['github_hash_commit'] = tag.commit.hexsha
       
        return metrics
    
    def _normalize_tag(self, repo: Repo, version: str) -> Optional[str]:
        """Normalize tag name and check if it exists in the repository"""
        tag_name = version
        if f"v{version}" in repo.tags:
            tag_name = f"v{version}"
        elif version not in repo.tags:
            return None
        return tag_name
    
    def _parse_date(self, date_str: str) -> datetime:
        if not date_str:
            return AccountAnalyzer.UTC_MIN_DATETIME
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
            return AccountAnalyzer.UTC_MIN_DATETIME