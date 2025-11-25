import json
import subprocess
from pathlib import Path
from typing import List, Optional
from git import Repo

class NPMClient:
    """Cloning Git repos associated with a pkg and retrieving ordered tags"""
    
    def get_package_git_url(self, package_name: str) -> Optional[str]:
        """Get the Git repo URL associated with an NPM pkg"""

        try:
            # Asks NPM for package metadata and gets the repository URL
            result = subprocess.run(
                ['npm', 'view', package_name, 'repository.url', '--json'],
                capture_output=True,
                text=True,
                check=True
            )
            git_url = json.loads(result.stdout.strip())

            if not git_url:
                return None

            # Normalize the URL: removes git, readme and any final hash
            git_url = git_url.replace("git+", "").replace("#readme", "").split("#")[0].rstrip("/")
            # Remove .git extension if present
            if git_url.endswith(".git"):
                git_url = git_url[:-4]

            return git_url

        except Exception as e:
            print(f"Error retrieving Git URL for {package_name}: {e}")
            return None

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