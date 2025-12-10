from pathlib import Path
from typing import List, Tuple
from git import Repo

from models import *
from comparators import VersionComparator
from utils import FileHandler, CalculateDiffs
from .code_analyzer import CodeAnalyzer

class GitVersionAnalyzer:
    """Handles analysis of versions from a Git repository"""

    def __init__(self, code_analyzer: CodeAnalyzer, file_handler: FileHandler):
        self.code_analyzer = code_analyzer
        self.file_handler = file_handler
        self.version_comparator = VersionComparator()
        self._previous_contents = {}
    
    def analyze_git_versions(self, package_name: str, repo: Repo) -> Tuple[List[FileMetrics], List[RedFlagChanges]]:
        """Analyze all Git versions of the package"""
        
        tags = sorted(repo.tags, key=lambda t: t.commit.committed_datetime)
        if not tags:
            print(f"No tags found for {package_name}")
            return [], []

        print(f"Found {len(tags)} Git tags")
        
        all_metrics = []
        all_changes = []
        prev_metrics = []
        repo_path = Path(repo.working_tree_dir)

        for i, tag in enumerate(tags, 1):
            print(f"  [{i}/{len(tags)}] Tag {tag.name}")
            try:
                repo.git.checkout(tag.name, force=True)
                curr_metrics = self._analyze_version(package_name, tag.name, repo_path)
                all_metrics.extend(curr_metrics)
                print(f"    Analyzed {len(curr_metrics)} files")

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
        #js_files = self.file_handler.get_js_files(package_dir)
        files = self.file_handler.get_all_files(package_dir)

        for file_path in files:
            try:
                rel_path = str(file_path.relative_to(package_dir))
                content = self.file_handler.read_file(file_path)

                # Calculating the diff with the previous version
                previous_content = self._previous_contents.get(rel_path)
                diffs_additions, diffs_deletions = CalculateDiffs.calculate_file_diffs(previous_content, content)

                package_info = {
                    'name': package_name,
                    'version': normalized_version,
                    'git_repo_path': str(package_dir),
                    'file_name': rel_path,
                    'info': "git"
                }
                release_info = {
                    'package_name': package_name,
                    'version': normalized_version,
                    'git_repo_path': str(package_dir)
                }
                
                file_metrics = self.code_analyzer.analyze_file(
                    content, 
                    package_info=package_info,
                    release_info=release_info,
                    file_diff_additions=diffs_additions,
                    file_diff_deletions=diffs_deletions
                )

                metrics = FileMetrics(
                    package=package_name,
                    version=normalized_version,
                    file_path=rel_path,
                    changes_additions= diffs_additions,
                    changes_deletions= diffs_deletions,
                    **file_metrics
                )
                metrics_list.append(metrics)
                self._previous_contents[rel_path] = content
            except Exception as e:
                print(f"Error analyzing {file_path}: {e}")

        return metrics_list