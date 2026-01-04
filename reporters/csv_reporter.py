import csv
from pathlib import Path
from typing import List, Union, TypeVar
from dataclasses import asdict, is_dataclass
from utils import synchronized_print

T = TypeVar('T')

class CSVReporter:
    """Generate CSV files with analysis results"""

    @staticmethod
    def save_csv(output_path: Path, data: Union[T, List[T]], append: bool = True) -> None:
        items = data if isinstance(data, list) else [data]
        
        if not items:
            synchronized_print(f"No data to save in {output_path}")
            return
        
        try:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            if not all(is_dataclass(item) for item in items):
                synchronized_print(f"Error: Not all items are dataclass instances for {output_path}")
                return
            
            file_exists = output_path.exists()
            mode = "a" if append else "w"
            
            with open(output_path, mode, newline='', encoding='utf-8') as f:
                fieldnames = asdict(items[0]).keys()
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                
                if not append or not file_exists:
                    writer.writeheader()
                
                for item in items:
                    writer.writerow(asdict(item))
                    
        except Exception as e:
            synchronized_print(f"Error saving CSV to {output_path}: {e}")
            return