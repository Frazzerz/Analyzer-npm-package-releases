from pathlib import Path
from typing import List, Tuple

from models import *
from utils import NPMClient, FileHandler
from .git_version_analyzer import GitVersionAnalyzer
from .local_version_analyzer import LocalVersionAnalyzer  
from .code_analyzer import CodeAnalyzer

class PackageAnalyzer:
    """Coordinator for analyzing Git and local versions of an npm package"""
    
    def __init__(self, include_local: bool = False, local_versions_dir: str = "./other_versions"):
        self.npm_client = NPMClient()
        self.file_handler = FileHandler()
        self.code_analyzer = CodeAnalyzer()
        self.include_local = include_local
        self.git_analyzer = GitVersionAnalyzer(self.code_analyzer, self.file_handler)
        self.local_analyzer = LocalVersionAnalyzer(self.code_analyzer, self.file_handler, local_versions_dir)
    
    def analyze_package(self, package_name: str) -> Tuple[List[FileMetrics], List[RedFlagChanges]]:
        """Analyze all releases of a package"""
        all_metrics = []
        all_changes = []
        
        # Analyze Git versions
        repo = self.npm_client.clone_package_repo(package_name)
        if repo:
            git_metrics, git_changes = self.git_analyzer.analyze_git_versions(package_name, repo)
            all_metrics.extend(git_metrics)
            all_changes.extend(git_changes)
        else:
            print(f"Unable to analyze {package_name} - Git repository not available")
        
        # If requested, analyze local versions
        if self.include_local:
            self.local_analyzer.setup_local_versions(package_name)
            local_metrics, local_changes = self.local_analyzer.analyze_local_versions(package_name)
            all_metrics.extend(local_metrics)
            all_changes.extend(local_changes)
        
        return all_metrics, all_changes