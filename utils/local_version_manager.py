import os
import re
import tarfile
from pathlib import Path
from typing import List, Dict, Optional

class LocalVersionManager:
    """Manages loading and extracting local versions."""
    
    def __init__(self, local_versions_dir: str = "./other_versions"):
        self.local_versions_dir = Path(local_versions_dir)
        self.local_extract_dir = self.local_versions_dir / "extracted"
    
    def get_local_versions_for_package(self, package_name: str) -> List[Dict]:
        """Finds all local versions for a package."""
        if not self.local_versions_dir.exists():
            return []
        
        package_short = package_name.split('/')[-1].lower()
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
        """Parses the filename to extract package and version."""
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
        """Checks if the string is a valid version."""
        return bool(re.match(r'^\d+\.\d+', version_str))    # Begin with one or more digits, followed by a dot , followed by one or more digits and they may have something else after them
    
    def extract_local_version(self, local_version_info: Dict, destination_dir: Path) -> Path:
        """Extracts a local version."""
        tgz_path = local_version_info['path']
        version = local_version_info['version']
        package = local_version_info.get('package_detected', 'unknown')
        
        extract_path = destination_dir / f"{package}-{version}-local"
        extract_path.mkdir(parents=True, exist_ok=True)
        
        with tarfile.open(tgz_path, 'r:gz') as tar:
            tar.extractall(path=extract_path)
        
        return extract_path
    
    def normalize_local_file_path(self, file_path: str) -> str:
        """Normalizes local file paths."""
        path = Path(file_path)
        parts = path.parts
        
        if 'extracted' in parts:
            extracted_idx = parts.index('extracted')
            if extracted_idx + 1 < len(parts):
                version_folder = parts[extracted_idx + 1]
                
                # Extract package name from version folder, remove version and suffix
                if version_folder.endswith('-local'):
                    package_base = re.sub(r'-\d+\.\d+\.\d+.*$', '', version_folder[:-6])
                else:
                    package_base = re.sub(r'-\d+\.\d+\.\d+.*$', '', version_folder)
                
                # Relative path after the version folder
                rest = parts[extracted_idx + 2:]
                
                # Remove 'package' directory if present
                if rest and rest[0] == 'package':
                    rest = rest[1:]
                
                if rest:
                    return str(Path(f"{package_base}-local", *rest))
        
        return str(path)