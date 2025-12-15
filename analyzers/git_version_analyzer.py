from pathlib import Path
from typing import List, Tuple
from git import Repo
import multiprocessing as mp
from models import *
from utils import FileHandler, synchronized_print
from .code_analyzer import CodeAnalyzer

class GitVersionAnalyzer:
    """Handles analysis of versions from a Git repository"""

    def __init__(self, code_analyzer: CodeAnalyzer, file_handler: FileHandler, max_processes: int = 1):
        self.code_analyzer = code_analyzer
        self.file_handler = file_handler
        self.max_processes = max_processes
    
    def analyze_git_versions(self, package_name: str, repo: Repo) -> List[FileMetrics]:
        """Analyze all Git versions of the package"""

        tags = sorted(repo.tags, key=lambda t: t.commit.committed_datetime)
        if not tags:
            synchronized_print(f"No tags found for {package_name}")
            return []

        synchronized_print(f"Found {len(tags)} Git tags")
        
        all_metrics = []
        repo_path = Path(repo.working_tree_dir)

        for i, tag in enumerate(tags):

            synchronized_print(f"  [{i+1}/{len(tags)}] Analyzing tag {tag.name}")
            try:
                repo.git.checkout(tag.name, force=True)
                curr_metrics = self._analyze_version(package_name, tag.name, repo_path)
                
                synchronized_print(f"    Analyzed {len(curr_metrics)} files")
                all_metrics.extend(curr_metrics)
                
            except Exception as e:
                print(f"Error analyzing tag {tag.name}: {e}")

        return all_metrics

    def _analyze_version(self, package_name: str, version: str, package_dir: Path) -> List[FileMetrics]:
        """Analyze all files of a specific Git version"""

        normalized_version = version[1:] if version.startswith('v') else version  # Remove initial 'v' if present

        files = self.file_handler.get_all_files(package_dir)
        
        if self.max_processes > 1:
            file_results = self._analyze_files_parallel(files, package_name, normalized_version, package_dir)
        else:
            file_results = self._analyze_files_sequential(files, package_name, normalized_version, package_dir)
        
        # Filter out None results (failed analyses)
        valid_results = [r for r in file_results if r is not None]
        # print(f"Version {normalized_version}: {len(valid_results)} files analyzed")
        return valid_results

    def _analyze_files_sequential(self, files: List[Path], package_name: str, version: str, package_dir: Path) -> List[FileMetrics]:
        """Sequential analysis of files."""
        results = []
        for file_path in files:
            try:
                result = self._analyze_single_file(file_path, package_name, version, package_dir)
                results.append(result)
            except Exception as e:
                print(f"Error analyzing {file_path}: {e}")
                results.append(None)
        return results

    def _analyze_files_parallel(self, files: List[Path], package_name: str, version: str, package_dir: Path) -> List[FileMetrics]:
        """Parallel analysis of files."""
        # Prepare arguments for each file
        args_list = []
        for file_path in files:
            args_list.append((file_path, package_name, version, package_dir))
        
        # Use multiprocessing Pool
        with mp.Pool(processes=self.max_processes) as pool:
            results = pool.starmap(self._analyze_single_file_wrapper, args_list)
        
        return results

    def _analyze_single_file_wrapper(self, file_path: Path, package_name: str, version: str, package_dir: Path) -> FileMetrics:
        """Wrapper function for parallel execution that handles exceptions."""
        try:
            return self._analyze_single_file(file_path, package_name, version, package_dir)
        except Exception as e:
            print(f"Error analyzing {file_path}: {e}")
            return None

    def _analyze_single_file(self, file_path: Path, package_name: str, version: str, package_dir: Path) -> FileMetrics:
        """Analyze a single file."""
        rel_path = str(file_path.relative_to(package_dir))
        content = self.file_handler.read_file(file_path)

        package_info = {
            'name': package_name,
            'version': version,
            'git_repo_path': str(package_dir),
            'file_name': rel_path,
            'info': "git"
        }
        
        file_metrics = self.code_analyzer.analyze_file(
            content, 
            package_info=package_info
        )

        metrics = FileMetrics(
            package=package_name,
            version=version,
            file_path=rel_path,
            **file_metrics
        )
        return metrics