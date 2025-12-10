from datetime import datetime, timezone
from typing import Dict, Optional
from git import Repo
from utils import NPMClient

class ReleaseAnalyzer:
    """Analyzes release integrity anomalies"""
    
    def __init__(self):
        self.npm_client = NPMClient()
        self._release_cache = {}
    
    def analyze(self, release_info: Dict) -> Dict:
        
        # For local versions or deobfuscated versions
        if not release_info or release_info == "local" or release_info == "deobfuscated":
            return self._empty_metrics()
        
        package_name = release_info.get('package_name', '')
        version = release_info.get('version', '')
        git_repo_path = release_info.get('git_repo_path')

        if not package_name or not version or not git_repo_path:
            return self._empty_metrics()
        
        # If the package is NOT cached, fetch it from NPM
        if package_name not in self._release_cache:
            self._release_cache[package_name] = self.npm_client.get_npm_package_data(package_name)
        
        # Use cached data (whether just added or already present)
        npm_data = self._release_cache[package_name]
        if not npm_data:
            return self._empty_metrics()
        
        metrics = {
            'npm_release_date': self._get_npm_release_time(npm_data, version),
            'github_release_date':  self._get_github_release_time(git_repo_path, version),
            'hash_npm': self._get_hash_npm(npm_data, version),
            'hash_github': self._get_hash_github(git_repo_path, version),
            'malicious_issues': self._get_malicious_issues_count(git_repo_path)                        # TODO
        }
        
        return metrics
    
    def _empty_metrics(self) -> Dict:
        return {
            'npm_release_date': datetime.min,       # missing date
            'github_release_date': datetime.min,    # missing date
            'hash_npm': "",
            'hash_github': "",
            'malicious_issues': 0
        }
    
    def _normalize_tag(self, repo: Repo, version: str) -> Optional[str]:
        """Normalize tag name and check if it exists in the repository"""
        tag_name = version
        if f"v{version}" in repo.tags:
            tag_name = f"v{version}"
        elif version not in repo.tags:
            return None
        return tag_name
    
    def _get_npm_release_time(self, npm_data: Dict, version: str) -> str:
        """Get the release time of a specific version from NPM data  -  2021-11-04T10:48:12.060Z"""
        try:
            if 'time' not in npm_data or version not in npm_data['time']:
                return ""
                
            return self._parse_date(npm_data['time'][version])
        except Exception as e:
            print(f"Error getting NPM release time: {e}")
            return ""

    def _get_github_release_time(self, repo_path: str, version: str) -> str:
        """Get the release time from GitHub repository  -  2021-11-04T17:48:07+07:00"""
        try:
            repo = Repo(repo_path)
            
            tag_name = self._normalize_tag(repo, version)
            if not tag_name:
                return ""
            
            tag = repo.tags[tag_name]
            commit = tag.commit
            return self._parse_date(commit.committed_datetime.isoformat())
            
        except Exception as e:
            print(f"Error getting GitHub release time for {version}: {e}")
            return ""
    
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

    def _get_hash_npm(self, npm_data: Dict, version: str) -> str:
        """Get the gitHead (commit hash) for a specific version from NPM data"""
        try:
            if 'versions' not in npm_data or version not in npm_data['versions']:
                return ""
            
            version_data = npm_data['versions'][version]
            return version_data.get('gitHead', "")
            #dist_info = npm_data['versions'][version].get('dist', {})      # SHA1
            #return dist_info.get('shasum', "")
        except Exception as e:
            print(f"Error getting  NPM gitHead: {e}")
            return ""

    def _get_hash_github(self, repo_path: str, version: str) -> str:
        """Get the integrity hash from GitHub repository"""
        try:
            repo = Repo(repo_path)
            
            tag_name = self._normalize_tag(repo, version)
            if not tag_name:
                return ""
            
            tag = repo.tags[tag_name]
            return tag.commit.hexsha            # SHA1
            
        except Exception as e:
            print(f"Error getting GitHub commit hash for {version}: {e}")
            return ""

    def _get_malicious_issues_count(self, repo_path: str) -> int:
        """Count the number of malicious issues in the GitHub repository"""
        # TODO
        return 0