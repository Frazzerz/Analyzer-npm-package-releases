import csv
from pathlib import Path
from typing import List, Any
from dataclasses import asdict

class CSVReporter:
    """Generate CSV files with analysis results"""

    @staticmethod
    def _save_csv(output_path: Path, items: List[Any], empty_message: str, append: bool = False) -> None:
        """Generic CSV saving utility"""
        if not items:
            print(empty_message.format(output_path=output_path))
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
        
    @staticmethod
    def save_metrics_single_file(output_path: Path, metrics: List[Any]) -> None:
        CSVReporter._save_csv(
            output_path,
            metrics,
            empty_message="No metrics to save in {output_path}",
            append=True
        )