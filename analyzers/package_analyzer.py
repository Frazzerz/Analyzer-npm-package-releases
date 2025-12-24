from pathlib import Path
from models import *
from utils import NPMClient, FileHandler
from .git_version_analyzer import GitVersionAnalyzer
from .code_analyzer import CodeAnalyzer

class PackageAnalyzer:
    """Coordinator for analyzing Git and local versions of an npm package"""
    
    def __init__(self, include_local: bool = False, local_versions_dir: str = "./other_versions", workers: int = 1):
        self.npm_client = NPMClient()
        self.file_handler = FileHandler()
        self.code_analyzer = CodeAnalyzer()
        self.include_local = include_local
        self.git_analyzer = GitVersionAnalyzer(self.code_analyzer, self.file_handler, workers, include_local=include_local, local_versions_dir=local_versions_dir)
        self.workers = workers
    
    def analyze_package(self, package_name: str, output_dir: Path) -> None:
        """Analyze all releases of a package"""

        repo = self.npm_client.clone_package_repo(package_name)
        if repo:
            self.git_analyzer.analyze_git_versions(package_name, repo, output_dir)
        else:
            print(f"Unable to analyze {package_name} - Git repository not available")
        
        return None