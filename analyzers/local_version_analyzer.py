from utils import FileHandler, LocalVersionManager, synchronized_print
from .code_analyzer import CodeAnalyzer

'''
def version_key(tag: str):
    """Sort key for versions that handles numeric parts and local suffixes."""
    is_local = "-local" in tag
    core = tag.replace("-local", "") if is_local else tag
    core = core[1:] if core.startswith("v") else core

    parts = []
    for p in core.split('.'):
        try:
            # Handles parts with suffixes like "1.0.0-beta"
            if '-' in p:
                main_part, suffix = p.split('-', 1)
                parts.append(int(main_part))
                parts.append(('suffix', suffix))
            else:
                parts.append(int(p))
        except ValueError:
            parts.append(9999)      # non-numeric values ​​sent to the end

    return (parts, 0 if is_local else 1, tag)  # local before others
'''
class LocalVersionAnalyzer:
    """Manages the analysis of local versions."""
    def __init__(self, code_analyzer: CodeAnalyzer, file_handler: FileHandler, local_versions_dir: str):
        self.code_analyzer = code_analyzer
        self.file_handler = file_handler
        self.local_version_manager = LocalVersionManager(local_versions_dir)
        self._local_versions = {}

    def setup_local_versions(self, package_name: str):
        """Sets up local versions for analysis."""
        local_versions = self.local_version_manager.get_local_versions_for_package(package_name)
        if not local_versions:
            synchronized_print(f"No local versions found for {package_name}")
            return

        synchronized_print(f"Found {len(local_versions)} local versions for {package_name}")
        self.local_version_manager.local_extract_dir.mkdir(parents=True, exist_ok=True)

        for local_version in local_versions:
            try:
                extracted_path = self.local_version_manager.extract_local_version(
                    local_version,
                    self.local_version_manager.local_extract_dir
                )
                version_with_suffix = f"{local_version['version']}-local"
                self._local_versions[version_with_suffix] = extracted_path
                synchronized_print(f"Added local version {version_with_suffix}")
            except Exception as e:
                synchronized_print(f"Error extracting {local_version['filename']}: {e}")
'''
    def analyze_local_versions(self, package_name: str) -> List[FileMetrics]:
        """Analyzes all local versions of the package."""
        if not self._local_versions:
            return []

        print(f"Analyzing {len(self._local_versions)} local versions")
        all_metrics = []

        sorted_versions = sorted(self._local_versions.keys(), key=version_key)

        #for version in sorted_versions:
        for i, version in enumerate(sorted_versions, 1):
            package_dir = self._local_versions[version]
            #print(f"  Local version {version}")
            synchronized_print(f"  [{i}/{len(sorted_versions)}] Analyzing {package_name} - Local version: {version}")
            try:
                curr_metrics = self._analyze_version(package_name, version, package_dir)
                all_metrics.extend(curr_metrics)
                print(f"    Analyzed {len(curr_metrics)} files")

            except Exception as e:
                print(f"Error analyzing local version {version}: {e}")

        return all_metrics

    def _analyze_version(self, package_name: str, version: str, package_dir: Path) -> List[FileMetrics]:
        """Analyzes all files of a specific local version."""
        metrics_list = []

        actual_package_dir = package_dir
        if (package_dir / 'package').exists():
            actual_package_dir = package_dir / 'package'

        files = self.file_handler.get_all_files(actual_package_dir)

        for file_path in files:
            try:
                rel_path = self.local_version_manager.normalize_local_file_path(
                    str(file_path.relative_to(actual_package_dir))
                )
                content = self.file_handler.read_file(file_path)
                
                package_info = {
                    'name': package_name,
                    'version': version,      # Local version indicator included
                    'file_name': rel_path,
                    'info': "local"
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
                metrics_list.append(metrics)
            except Exception as e:
                print(f"Error analyzing {file_path}: {e}")

        return metrics_list
'''