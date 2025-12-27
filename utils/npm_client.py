from pathlib import Path
from typing import Dict, Optional
from git import Repo
import requests
import subprocess
import os
from .logging_utils import synchronized_print

class NPMClient:
    """Cloning Git repos associated with a pkg and retrieving ordered tags"""
    def __init__(self, registry_url: str = "https://registry.npmjs.org"):
        self.registry_url = registry_url
        
    def get_npm_package_data(self, package_name: str) -> Optional[Dict]:
        """Fetch raw metadata for an NPM package by making an HTTP request to the registry"""
        try:
            response = requests.get(f'{self.registry_url}/{package_name}', timeout=5)
            response.raise_for_status()
            return response.json()
        
        except requests.exceptions.RequestException as e:
            print(f"Failed to fetch '{package_name}': {e}")
            return None
    
    def get_package_git_url(self, package_name: str) -> Optional[str]:
        """Extracts and normalizes the Git repository URL for an NPM package"""
        '''
        try:
            # Asks NPM for package metadata and gets the repository URL
            result = subprocess.run(
                ['npm', 'view', package_name, 'repository.url', '--json'],
                capture_output=True,
                text=True,
                check=True
            )
            git_url = json.loads(result.stdout.strip())
        '''
        data = self.get_npm_package_data(package_name)
        if not data:
            return None
        
        git_url = data.get('repository', {}).get('url', '')
        if not git_url:
            return None

        # Remove common prefixes
        prefixes = ["git+https://", "git+ssh://", "git://", "git+","ssh://git@", "http://"]

        for prefix in prefixes:
            if git_url.startswith(prefix):
                git_url = git_url[len(prefix):]
        
        # Remove any fragment (#readme, #master, etc.)
        git_url = git_url.split('#')[0]
        
        # For GitHub URLs
        if 'github.com' in git_url:
            # Ensure it starts with https://
            if not git_url.startswith('https://'):
                git_url = f'https://{git_url}'
            # Ensure it ends with .git
            if not git_url.endswith('.git'):
                git_url = f'{git_url}.git'
        git_url = git_url.rstrip('/')
        
        return git_url

    def clone_package_repo(self, package_name: str, repos_dir: Path = Path("repos")) -> Optional[Repo]:
        """Clone an NPM package's Git repository in the `repos/` directory. If the repository has already been cloned previously, reuse it"""
        
        git_url = self.get_package_git_url(package_name)
        if not git_url:
            print(f"No Git URL found for {package_name}")
            return None

        repos_dir.mkdir(exist_ok=True)
        repo_name = package_name.replace('/', '_')
        repo_path = repos_dir / repo_name

        # Reuse the repository if it already exists
        if repo_path.exists() and (repo_path / ".git").exists():
            print(f"Existing repository found for {package_name}")
            return Repo(repo_path)

        try:
            
            # Set environment variables to prevent interactive authentication
            #env = os.environ.copy()
            #env['GIT_TERMINAL_PROMPT'] = '0'  # Disable interactive prompt
            #env['GIT_ASKPASS'] = 'echo'       # Return empty password
            synchronized_print(f"Cloning repository for {package_name} from {git_url}...")
            '''
            # Clone with GitPython, no timeout
            repo = Repo.clone_from(git_url, repo_path)
            synchronized_print(f"Repository cloned for {package_name}")
            return repo
            '''
            # Clone with subprocess, with timeout
            result = subprocess.run(
                ['git', 'clone', git_url, str(repo_path)],
                capture_output=True,
                text=True,
                timeout=120, # seconds
                env={**os.environ, 'GIT_TERMINAL_PROMPT': '0'}
            )
            if result.returncode == 0:
                synchronized_print(f"Repository cloned for {package_name}")
                return Repo(repo_path)

        except Exception as e:
            
            error_msg = str(e).lower()
            if 'authentication' in error_msg or 'credentials' in error_msg:
                print(f"Repository for {package_name} requires authentication")
            elif 'timed out' in error_msg:
                print(f"Cloning repository for {package_name} timed out")
            else:
                print(f"Error cloning {package_name}: {e}")
            # Alternative tests could be done to try to download it via other means

            # Clean up partial clone if it exists
            if repo_path.exists():
                import shutil
                try:
                    shutil.rmtree(repo_path)
                except:
                    pass    
            return None