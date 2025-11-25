from pathlib import Path
from typing import List, Tuple
from git import Repo

from models import *
from comparators import VersionComparator
from utils import FileHandler
from .code_analyzer import CodeAnalyzer

class GitVersionAnalyzer:
    """Handles analysis of versions from a Git repository"""

    def __init__(self, code_analyzer: CodeAnalyzer, file_handler: FileHandler):
        self.code_analyzer = code_analyzer
        self.file_handler = file_handler
        self.version_comparator = VersionComparator()
    
    def analyze_git_versions(self, package_name: str, repo: Repo) -> Tuple[List[FileMetrics], List[RedFlagChanges]]:
        """Analyze all Git versions of the package"""
        
        tags = sorted(repo.tags, key=lambda t: t.commit.committed_datetime)
        if not tags:
            print(f"No tags found for {package_name}")
            return [], []

        print(f"Found {len(tags)} Git tags")
        
        all_metrics = []
        all_changes = []
        prev_metrics = None
        repo_path = Path(repo.working_tree_dir)

        for i, tag in enumerate(tags, 1):
            print(f"  [{i}/{len(tags)}] Tag {tag.name}")
            try:
                repo.git.checkout(tag.name, force=True)
                curr_metrics = self._analyze_version(package_name, tag.name, repo_path)
                all_metrics.extend(curr_metrics)
                print(f"    Analyzed {len(curr_metrics)} files")

                if prev_metrics:
                    changes = self.version_comparator.compare_versions(prev_metrics, curr_metrics)
                    all_changes.extend(changes)

                prev_metrics = curr_metrics
            except Exception as e:
                print(f"Error analyzing tag {tag.name}: {e}")

        return all_metrics, all_changes

    def _analyze_version(self, package_name: str, version: str, package_dir: Path) -> List[FileMetrics]:
        """Analyze all files of a specific Git version"""

        normalized_version = version[1:] if version.startswith('v') else version   # Remove initial 'v' if present

        metrics_list = []
        js_files = self.file_handler.get_js_files(package_dir)

        for file_path in js_files:
            try:
                rel_path = str(file_path.relative_to(package_dir))
                content = self.file_handler.read_file(file_path)
                
                # Info for NPM
                package_info = {
                    'name': package_name,
                    'version': normalized_version,
                    'git_repo_path': str(package_dir)
                }
                release_info = {
                    'package_name': package_name,
                    'version': normalized_version,
                    'git_repo_path': str(package_dir)
                }
                
                file_metrics = self.code_analyzer.analyze_file(     # TODO Ora package_info e release_info sono uguali, ma in futuro potrebbero differire
                    content, 
                    package_info=package_info,
                    release_info=release_info
                )

                metrics = FileMetrics(
                    package=package_name,
                    version=normalized_version,
                    file_path=rel_path,
                    **file_metrics
                )
                metrics_list.append(metrics)
            except Exception as e:
                print(f"Error analyzing {file_path}: {e}")
        return metrics_list