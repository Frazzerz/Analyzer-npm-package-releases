from pathlib import Path
from typing import List
import json
import shutil
import os
class FileHandler:
    """Handles file and directory operations"""
    
    @staticmethod
    def load_packages_from_json(path: str) -> List[str]:
        """Load package names from a JSON file"""        
        try:
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return [data] if isinstance(data, str) else data
        except Exception as e:
            raise SystemExit(f"Error reading JSON {path}: {e}")
        
    @staticmethod
    def get_js_files(directory: Path) -> List[Path]:
        """Find all JavaScript files in directory (recursive)"""
        return list(directory.rglob('*.js'))
    
    @staticmethod
    def get_all_files(directory: Path) -> List[Path]:
        """Find all files in directory (recursive) excluding certain directories, files and extensions."""
        # Excluded: Also auto-generated file (like yarn.lock)
        # not excluded: README.md, package.json, all .js .mjs .ts .cjs .js.map files
        exclude_dirs = {'.git', 'node_modules', '.github', '__tests__', 'test', 'tests'}
        exclude_files = {
            'LICENSE', '.npmrc', '.editorconfig', '.gitattributes', 'license',
            '.eslintrc', '.prettierrc', 'CHANGELOG.md', '.eslintignore', 'yarn.lock', '.gitignore'
        }
        exclude_suffixes = ('.d.ts', '.d.ts.map')

        files: List[Path] = []
        directory_str = str(directory)
        for root, dirs, filenames in os.walk(directory_str):
            # dirs contains names (not full paths)
            dirs[:] = [d for d in dirs if d not in exclude_dirs]
            for name in filenames:
                if name in exclude_files:
                    continue
                if name.endswith(exclude_suffixes):
                    continue

                files.append(Path(root) / name)

        return files
    
    @staticmethod
    def read_file(file_path: Path) -> str:
        """Read file content"""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                return f.read()
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
            return ""
    
    @staticmethod
    def ensure_directory(directory: Path) -> None:
        """Create directory if it doesn't exist"""
        directory.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def delete_previous_analysis() -> None:
        """Delete all results from previous analysis (deobfuscated_files, repos, other_versions/extracted, log file, output directory"""

        dirs_to_delete = ['deobfuscated_files', 'repos', 'other_versions/extracted', 'analysis_results']
        for dir_name in dirs_to_delete:
            dir_path = Path(dir_name)
            if dir_path.exists() and dir_path.is_dir():
                shutil.rmtree(dir_path)
                print(f"Deleted directory: {dir_path}")

        log_file = Path('log.txt')
        if log_file.exists() and log_file.is_file():
            log_file.unlink()
            print(f"Deleted log file: {log_file}")
