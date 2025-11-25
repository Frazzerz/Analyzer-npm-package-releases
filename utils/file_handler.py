from pathlib import Path
from typing import List
import json

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
        """Find all files in directory (recursive) excluding .git and node_modules directories"""
        exclude = {'.git', 'node_modules', '.editorconfig', '.npmrc', '.gitattributes', '.github', 'license'}
        return [file for file in directory.rglob('*') 
                if file.is_file() 
                and not any(part in exclude for part in file.parts)]
    
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