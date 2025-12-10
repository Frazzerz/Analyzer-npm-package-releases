from typing import Dict
from git import Repo
from utils import NPMClient

class AccountAnalyzer:
    """Analyzes account compromise"""
    
    def __init__(self):
        self.npm_client = NPMClient()
        self._package_cache = {}
    
    def analyze(self, package_info: Dict) -> Dict:
                  
        package_name = package_info.get('name', '')
        version = package_info.get('version', '')
        git_repo_path = package_info.get('git_repo_path')
        
        # For local versions or deobfuscated versions
        if not package_info or package_info == "local" or package_info == "deobfuscated":
            return self._empty_metrics()
        
        # If the package is NOT cached, fetch it from NPM
        if package_name not in self._package_cache:
            self._package_cache[package_name] = self.npm_client.get_npm_package_data(package_name)
        
        # Use cached data (whether just added or already present)
        npm_data = self._package_cache[package_name]
        if not npm_data:
            return self._empty_metrics()
        
        npm_metrics = self._get_npm_metrics(npm_data, version)
        github_metrics = self._get_github_metrics(git_repo_path)
        
        return {
            'npm_maintainers': npm_metrics['maintainers_count'],
            'npm_maintainers_nicks': npm_metrics['maintainers_nicks'],
            'npm_maintainers_emails': npm_metrics['maintainers_emails'],
            'npm_maintainer_pubblished_release': npm_metrics['published_release'],
            'github_contributors': github_metrics['contributors_count'],
            'github_contributors_nicks': github_metrics['contributors_nicks'],
            'github_contributors_emails': github_metrics['contributors_emails'],            
            'github_contributors_published_release': github_metrics['published_release'],           # TODO
            'github_owners': github_metrics['owners']                                               # TODO
        }
    
    def _empty_metrics(self) -> Dict:
        return {
            'npm_maintainers': 0,
            'npm_maintainers_nicks': [],
            'npm_maintainers_emails': [],
            'npm_maintainer_pubblished_release': '',
            'github_contributors': 0,
            'github_contributors_nicks': [],
            'github_contributors_emails': [],            
            'github_contributors_published_release': '',
            'github_owners': ''
        }
    
    def _get_npm_metrics(self, npm_data: Dict, version: str) -> Dict:
        """Returns all NPM metrics in a dictionary"""
        try:
            if 'versions' not in npm_data or version not in npm_data['versions']:
                return self._empty_npm_metrics()
                
            version_data = npm_data['versions'][version]
            maintainers = version_data.get('maintainers', [])                       # == owners
            nicks = [maintainer.get('name', '') for maintainer in maintainers if maintainer.get('name')]
            emails = [maintainer.get('email', '') for maintainer in maintainers if maintainer.get('email')]
            npm_user = version_data.get('_npmUser', {})
            published_release = npm_user.get('name', '') if npm_user else ''        # Blank space if no publisher found
            
            return {
                'maintainers_count': len(maintainers),
                'maintainers_nicks': nicks,
                'maintainers_emails': emails,
                'published_release': published_release
            }
        except Exception as e:
            print(f"Error getting NPM metrics: {e}")
            return self._empty_npm_metrics()
    
    def _get_github_metrics(self, repo_path: str) -> Dict:
        """Returns all GitHub metrics in a dictionary"""
        try:
            if not repo_path:
                return self._empty_github_metrics()
                
            repo = Repo(repo_path)
            
            contributors_names = set()
            contributors_emails = set()            
            for commit in repo.iter_commits():
                if commit.author:
                    contributors_names.add(commit.author.name)
                    contributors_emails.add(commit.author.email)
            
            names_list = list(contributors_names)
            emails_list = list(contributors_emails)
            
            published_release = ''                           # TODO DA CAPIRE MEGLIO
            owners = self._get_github_owner(repo)
            
            return {
                'contributors_count': len(contributors_names),
                'contributors_nicks': names_list,
                'contributors_emails': emails_list,
                'published_release': published_release,
                'owners': owners
            }
            
        except Exception as e:
            print(f"Error getting GitHub metrics: {e}")
            return self._empty_github_metrics()
    
    def _empty_npm_metrics(self) -> Dict:
        return {
            'maintainers_count': 0,
            'maintainers_nicks': [],
            'maintainers_emails': [],
            'published_release': ''
        }
    
    def _empty_github_metrics(self) -> Dict:
        return {
            'contributors_count': 0,
            'contributors_nicks': [],
            'contributors_emails': [],
            'published_release': '',
            'owners': ''
        }
    
    def _get_github_owner(self, repo: Repo) -> str:
        """Extracts the repository owner"""
        # TODO DA CAPIRE COME FARE
        return ''