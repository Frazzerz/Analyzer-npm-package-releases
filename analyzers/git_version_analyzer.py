from dataclasses import asdict
from pathlib import Path
from typing import Dict, List, Tuple
from git import Repo
import multiprocessing as mp
from models import *
from reporters.csv_reporter import CSVReporter
from utils import FileHandler, synchronized_print
from .aggregate_metrics_by_tag import AggregateMetricsByTag
from .code_analyzer import CodeAnalyzer
from comparators.version_comparator import VersionComparator

class GitVersionAnalyzer:
    """Handles analysis of versions from a Git repository"""

    def __init__(self, code_analyzer: CodeAnalyzer, file_handler: FileHandler, max_processes: int = 1):
        self.code_analyzer = code_analyzer
        self.file_handler = file_handler
        self.max_processes = max_processes
    
    def analyze_git_versions(self, package_name: str, repo: Repo, output_dir: Path) -> None:
        """Analyze all Git versions of the package"""

        tags = sorted(repo.tags, key=lambda t: t.commit.committed_datetime)
        if not tags:
            synchronized_print(f"No tags found for {package_name}")
            return []

        synchronized_print(f"Found {len(tags)} Git tags")
        
        previous_aggregate_metrics = []
        all_aggregate_metrics_by_tag = []
        repo_path = Path(repo.working_tree_dir)

        for i, tag in enumerate(tags):

            synchronized_print(f"  [{i+1}/{len(tags)}] Analyzing tag {tag.name}")
            try:
                repo.git.checkout(tag.name, force=True)
                curr_metrics = self._analyze_version(package_name, tag.name, repo_path)
                synchronized_print(f"    Analyzed {len(curr_metrics)} files")

                # aggregate_metrics_by_tag tutte le metriche aggregate per tutti i file per ogni versione (list[list[VersionMetrics]])
                # aggregate_metrics_by_tag è il corrente, Calculate also metrics for account categories
                aggregate_metrics_by_tag = AggregateMetricsByTag.aggregate_metrics_by_tag(curr_metrics, repo_path)
                #synchronized_print(f"aggregate: {aggregate_metrics_by_tag}")

                # all_aggregate_metrics tutte le metriche aggregate per tutti i file di tutte le versioni, tranne l'ultima (list[VersionMetrics])
                # all_aggregate_metrics_by_tag è la lista aggregata di tutte le versioni precedenti, viene aggiornato di volta in volta
                all_aggregate_metrics_by_tag, red_flags = self.calculate_red_flags(package_name, aggregate_metrics_by_tag, previous_aggregate_metrics, all_aggregate_metrics_by_tag)

                #synchronized_print(f"before previous_aggregate_metrics: {previous_aggregate_metrics}")
                previous_aggregate_metrics = list(aggregate_metrics_by_tag)
                #synchronized_print(f"after previous_aggregate_metrics: {previous_aggregate_metrics}")

                # Incremental save detailed metrics for the current tag. Avoid pass this mega list around
                all_metrics_csv = output_dir / "all_metrics.csv"
                flags_csv = output_dir / "red_flags.csv"
                aggregate_metrics_csv = output_dir / "aggregate_metrics_by_tag.csv"
                aggregate_metrics_history_csv = output_dir / "aggregate_metrics_history.csv"
                
                CSVReporter().save_metrics_single_file(all_metrics_csv, curr_metrics)
                CSVReporter().save_metrics_single_file(aggregate_metrics_csv, aggregate_metrics_by_tag)
                CSVReporter().save_metrics_single_file(aggregate_metrics_history_csv, all_aggregate_metrics_by_tag)
                CSVReporter().save_metrics_single_file(flags_csv, [red_flags])

            except Exception as e:
                print(f"Error analyzing tag {tag.name}: {e}")

        return
    

    def calculate_red_flags(self, package_name: str, current_metrics: List[VersionMetrics], previous_metrics: List[VersionMetrics], all_previous_metrics: List[VersionMetrics]) -> (List[RedFlag], VersionMetrics):
        
        comparator = VersionComparator()
        #synchronized_print(f"previous_metrics {previous_metrics}")
        
        # Prendiamo l'ultimo previous per il confronto
        prev_metrics_obj = previous_metrics[0] if previous_metrics else None
        curr_metrics_obj = current_metrics[0]

        # Converto in dict per il comparator
        prev_metrics_dict = prev_metrics_obj.__dict__ if prev_metrics_obj else None
        curr_metrics_dict = curr_metrics_obj.__dict__

        # Versioni per il red flag
        version_from = prev_metrics_obj.version if prev_metrics_obj else "first"
        version_to = curr_metrics_obj.version

        # all_previous_metrics come dict (se serve)
        all_prev_dict = {m.version: m.__dict__ for m in all_previous_metrics}

        # Chiamo il comparator
        red_flag = comparator.compare_tags(
            all_prev_tag_metrics=all_prev_dict,
            prev_tag_metrics=prev_metrics_dict,
            curr_tag_metrics=curr_metrics_dict,
            package=package_name,
            version_from=version_from,
            version_to=version_to
        )
        #synchronized_print(f"Red flags: {red_flag}")

        #synchronized_print(f"all_previous_metrics before aggregation: {all_previous_metrics}")  
        all_previous_metrics = AggregateMetricsByTag.aggregate_metrics_incremental(all_previous_metrics, current_metrics)
        #synchronized_print(f"all_previous_metrics after aggregation: {all_previous_metrics}")

        return all_previous_metrics, red_flag

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