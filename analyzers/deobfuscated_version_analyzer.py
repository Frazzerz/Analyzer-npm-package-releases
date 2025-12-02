from pathlib import Path
from typing import List, Tuple

from models import *
from comparators import VersionComparator
from utils import FileHandler
from .code_analyzer import CodeAnalyzer

class DeobfuscatedAnalyzer:
    """Analyzer for deobfuscated files of a package"""
    
    def __init__(self, code_analyzer: CodeAnalyzer, file_handler: FileHandler):
        self.code_analyzer = code_analyzer
        self.file_handler = file_handler
        self.version_comparator = VersionComparator()

    def analyze_deobfuscated_versions(self, package_name: str, deobf_dir: Path) -> Tuple[List[FileMetrics], List[RedFlagChanges]]:
        """Analyze all deobfuscated files for a package"""
        all_metrics = []
        all_changes = []
        
        version_dirs = self._get_deobfuscated_version_dirs(deobf_dir)
        if not version_dirs:
            return [], []

        print(f"Found deobfuscated files for package {package_name} in {len(version_dirs)} versions, analyzing...")

        prev_metrics = []
        sorted_versions = sorted(version_dirs.keys())

        for version in sorted_versions:
            version_dir = version_dirs[version]
            print(f"  Analyzing version: {version}")
            
            try:
                curr_metrics = self._analyze_version(package_name, version, version_dir)
                all_metrics.extend(curr_metrics)
                print(f"    Analyzed {len(curr_metrics)} deobfuscated files")
                
                #if prev_metrics:
                changes = self.version_comparator.compare_versions(prev_metrics, curr_metrics)
                all_changes.extend(changes)

                prev_metrics = curr_metrics
            except Exception as e:
                print(f"Error analyzing deobfuscated version {version}: {e}")
                
        return all_metrics, all_changes

    def _get_deobfuscated_version_dirs(self, deobf_dir: Path) -> dict:
        """Find all version subdirectories that contain deobfuscated files"""
        version_dirs = {}
        
        for item in deobf_dir.iterdir():
            if item.is_dir():
                # Check if this version directory contains any deobfuscated files
                has_deobfuscated_files = any(
                    f.is_file() and f.name.endswith('-deobfuscated.js') 
                    for f in item.iterdir()
                )
                if has_deobfuscated_files:
                    version_dirs[item.name] = item
                    
        return version_dirs

    def _analyze_version(self, package_name: str, version: str, version_dir: Path) -> List[FileMetrics]:
        """Analyze all deobfuscated files in a specific version directory"""
        metrics_list = []
        
        deobfuscated_files = [
            f for f in version_dir.iterdir() 
            if f.is_file() and f.name.endswith('-deobfuscated.js')
        ]
        
        for file_path in deobfuscated_files:
            try:
                content = self.file_handler.read_file(file_path)
                
                package_info = {
                    'name': package_name,
                    'version': version,
                    'file_name': file_path.name,
                    'info': "deobfuscated"
                }

                file_metrics = self.code_analyzer.analyze_file(
                    content, 
                    package_info=package_info, 
                    release_info="deobfuscated",
                    file_diff_additions='',
                    file_diff_deletions=''
                )

                metrics = FileMetrics(
                    package=package_name,
                    version=version,
                    file_path=str(file_path.relative_to(version_dir)),
                    changes_additions='',
                    changes_deletions='',
                    **file_metrics
                )
                metrics_list.append(metrics)
            except Exception as e:
                print(f"Error analyzing {file_path}: {e}")
                
        return metrics_list