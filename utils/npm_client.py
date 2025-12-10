from pathlib import Path
from typing import Dict, List, Optional
from git import Repo
import requests

class NPMClient:
    """Cloning Git repos associated with a pkg and retrieving ordered tags"""
    def __init__(self, registry_url: str = "https://registry.npmjs.org"):
        self.registry_url = registry_url
        
    def get_npm_package_data(self, package_name: str) -> Optional[Dict]:
        """Fetch raw metadata for an NPM package by making an HTTP request to the registry"""
        try:
            response = requests.get(f'{self.registry_url}/{package_name}', timeout=3)
            response.raise_for_status()
            return response.json()
        
        except requests.exceptions.RequestException as e:
            print(f"[NPM ERROR] Failed to fetch '{package_name}': {e}")
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
        # Normalize the URL: removes git, readme and any final hash
        git_url = git_url.replace("git+", "").replace("#readme", "")
        # Remove .git extension if present
        return git_url.split("#")[0].rstrip("/").rstrip(".git")

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
            # Clone the repository
            repo = Repo.clone_from(git_url, repo_path)
            print(f"Repository cloned for {package_name}")
            return repo
        except Exception as e:
            print(f"Error cloning {package_name}: {e}")
            return None

    def get_package_tags(self, repo: Repo) -> List[str]:
        """Return tags sorted chronologically"""
        
        try:
            tags = sorted(repo.tags, key=lambda t: t.commit.committed_datetime)
            return [t.name for t in tags]
        except Exception as e:
            print(f"Error retrieving tags: {e}")
            return []