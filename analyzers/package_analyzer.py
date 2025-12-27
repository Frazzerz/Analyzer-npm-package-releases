from pathlib import Path
from utils import NPMClient
from .git_version_analyzer import GitVersionAnalyzer

class PackageAnalyzer:
    """Coordinator for analyzing Git and local versions of an npm package"""
    
    def __init__(self, include_local: bool = False, local_versions_dir: str = "./other_versions", workers: int = 1, package_name: str = "", output_dir: Path = Path(".")):
        self.pkg_name = package_name
        self.output_dir = output_dir
        self.npm_client = NPMClient(pkg_name=package_name)
        self.git_analyzer = GitVersionAnalyzer(workers, include_local=include_local, local_versions_dir=local_versions_dir)
    
    def analyze_package(self) -> None:
        """Analyze all releases of a package"""

        repo = self.npm_client.clone_package_repo()
        if repo:
            self.git_analyzer.analyze_git_versions(self.pkg_name, repo, self.output_dir)
        else:
            print(f"Unable to analyze {self.pkg_name} - Git repository not available")