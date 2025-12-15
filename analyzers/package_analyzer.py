from pathlib import Path
from typing import Dict, List
from comparators.version_comparator import VersionComparator
from models import *
from utils import NPMClient, FileHandler
from .git_version_analyzer import GitVersionAnalyzer
from .local_version_analyzer import LocalVersionAnalyzer  
from .deobfuscated_version_analyzer import DeobfuscatedAnalyzer
from .code_analyzer import CodeAnalyzer

class PackageAnalyzer:
    """Coordinator for analyzing Git and local versions of an npm package"""
    
    def __init__(self, include_local: bool = False, local_versions_dir: str = "./other_versions", workers: int = 1):
        self.npm_client = NPMClient()
        self.file_handler = FileHandler()
        self.code_analyzer = CodeAnalyzer()
        self.include_local = include_local
        self.git_analyzer = GitVersionAnalyzer(self.code_analyzer, self.file_handler, workers)
        self.local_analyzer = LocalVersionAnalyzer(self.code_analyzer, self.file_handler, local_versions_dir)
        self.deobfuscated_analyzer = DeobfuscatedAnalyzer(self.code_analyzer, self.file_handler)
        self.workers = workers
    
    def analyze_package(self, package_name: str) -> List[FileMetrics]:
        """Analyze all releases of a package"""
        all_metrics = []
        
        # Analyze Git versions
        repo = self.npm_client.clone_package_repo(package_name)
        if repo:
            git_metrics = self.git_analyzer.analyze_git_versions(package_name, repo)
            all_metrics.extend(git_metrics)
        else:
            print(f"Unable to analyze {package_name} - Git repository not available")
        
        # If requested, analyze local versions
        if self.include_local:
            self.local_analyzer.setup_local_versions(package_name)
            local_metrics = self.local_analyzer.analyze_local_versions(package_name)
            all_metrics.extend(local_metrics)
        
        # If deobfuscated files were created during analysis, analyze them as well
        deobf_dir = Path('deobfuscated_files') / package_name
        if deobf_dir.exists() and deobf_dir.is_dir():
            deobf_metrics = self.deobfuscated_analyzer.analyze_deobfuscated_versions(package_name, deobf_dir)
            all_metrics.extend(deobf_metrics)
        
        return all_metrics
    
    def analyze_package_red_flags(self, package_name: str, aggregate_metrics_by_tag: Dict[str, Dict[str, int]]) -> List[RedFlagChanges]:
        """Analyze red flags across versions of a package using tag-level comparison"""
        comparator = VersionComparator()
        all_red_flags = []
        
        # Versions are already sorted by aggregate_metrics_by_version
        versions = list(aggregate_metrics_by_tag.keys())
        
        # Compare consecutive tags
        for i in range(len(versions)):
            current_version = versions[i]
            current_metrics = aggregate_metrics_by_tag[current_version]
            
            # Get previous version metrics (None for first version)
            previous_metrics = aggregate_metrics_by_tag[versions[i-1]] if i > 0 else None
            previous_version = versions[i-1] if i > 0 else "INITIAL"
            
            # Perform tag-level comparison
            tag_red_flags = comparator.compare_tags(
                previous_metrics, 
                current_metrics,
                package_name,
                previous_version,
                current_version
            )
            
            all_red_flags.append(tag_red_flags)
        
        return all_red_flags