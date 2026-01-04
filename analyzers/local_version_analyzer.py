from utils import synchronized_print
import os
import re
import tarfile
from pathlib import Path
from typing import List, Dict, Optional
from models import VersionEntry
from packaging.version import Version
from utils.logging_utils import OutputTarget

class LocalVersionAnalyzer:
    """Manages loading and extracting local versions"""
    def __init__(self, local_versions_dir: str = "./other_versions", pkg_name: str = ""):
        self.pkg_name = pkg_name
        self.local_versions_dir = Path(local_versions_dir)
        self.local_extract_dir = self.local_versions_dir / "extracted"
        self._local_versions = {}
        
    def setup_local_versions(self) -> None:
        """Sets up local versions for analysis"""
        local_versions = self._get_local_versions_for_package()
        if not local_versions:
            synchronized_print(f"No local versions found for {self.pkg_name}")
            return

        synchronized_print(f"Found {len(local_versions)} local versions for {self.pkg_name}", target=OutputTarget.FILE_ONLY)
        self.local_extract_dir.mkdir(parents=True, exist_ok=True)

        for local_version in local_versions:
            try:
                extracted_path = self._extract_local_version(
                    local_version,
                    self.local_extract_dir
                )
                version_with_suffix = f"{local_version['version']}+local"
                #version_with_suffix = f"v{local_version['version']}-local"
                #version_with_suffix = f"posthog-node@{local_version['version']}-local"
                self._local_versions[version_with_suffix] = extracted_path
                synchronized_print(f"Added local version {version_with_suffix}")
            except Exception as e:
                synchronized_print(f"Error extracting {local_version['filename']}: {e}")

    def _get_local_versions_for_package(self) -> List[Dict]:
        """Finds all local versions for a package"""
        if not self.local_versions_dir.exists():
            return []
        
        package_short = self.pkg_name.split('/')[-1].lower()
        local_versions = []
        
        for filename in os.listdir(self.local_versions_dir):
            if not filename.endswith('.tgz'):
                continue
            
            name_without_ext = filename[:-4]
            parsed = self._parse_local_filename(name_without_ext)
            
            if parsed:
                file_package, file_version = parsed
                if file_package.lower() == package_short:
                    full_path = self.local_versions_dir / filename
                    local_versions.append({
                        'version': file_version,
                        'path': full_path,
                        'filename': filename,
                        'package_detected': file_package
                    })
        
        return local_versions
    
    def _parse_local_filename(self, filename: str) -> Optional[tuple]:
        """Parses the filename to extract package and version"""
        cleaned = filename.lstrip('@')
        
        # Try format @package@version
        if '@' in cleaned:
            parts = cleaned.rsplit('@', 1)
            if len(parts) == 2:
                package, version = parts
                if self._is_valid_version(version):
                    return (package, version)
        
        # Try format package-version
        version_pattern = r'(\d+\.\d+\.\d+(?:[-._]?[a-zA-Z0-9]+)*)' # at least 3 numbers separated by periods and optionally allows suffixes like -alpha
        matches = list(re.finditer(version_pattern, filename))
        
        if matches:
            last_match = matches[-1]
            version = last_match.group(1)
            repo_end_idx = last_match.start()
            package = filename[:repo_end_idx].rstrip('-')
            if package and self._is_valid_version(version):
                return (package, version)
        
        return None
    
    def _is_valid_version(self, version_str: str) -> bool:
        """Checks if the string is a valid version"""
        return bool(re.match(r'^\d+\.\d+', version_str))    # Begin with one or more digits, followed by a dot , followed by one or more digits and they may have something else after them
    
    def _extract_local_version(self, local_version_info: Dict, destination_dir: Path) -> Path:
        """Extracts a local version"""
        tgz_path = local_version_info['path']
        version = local_version_info['version']
        package = local_version_info.get('package_detected', 'unknown')
        
        extract_path = destination_dir / f"{package}-{version}-local"
        extract_path.mkdir(parents=True, exist_ok=True)
        
        with tarfile.open(tgz_path, 'r:gz') as tar:
            tar.extractall(path=extract_path)
        
        return extract_path
    
    def unite_versions(self, entries: List[VersionEntry]) -> List[VersionEntry]:
        """Combines Git and local versions into a single sorted list of VersionEntry"""
        for v_name, path in self._local_versions.items():
            entries.append(VersionEntry(name=v_name,source="local",ref=path))
        return sorted(entries, key=lambda e: Version(str(e.name)))