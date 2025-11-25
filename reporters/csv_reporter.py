import csv
from pathlib import Path
from typing import List, Any
from dataclasses import asdict

class CSVReporter:
    """Generate CSV files with analysis results"""

    @staticmethod
    def _save_csv(output_path: Path, items: List[Any], empty_message: str) -> None:
        """Generic CSV saving utility"""
        if not items:
            print(empty_message.format(output_path=output_path))
            return
        
        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            fieldnames = asdict(items[0]).keys()
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(asdict(item) for item in items)

    @staticmethod
    def save_metrics(output_path: Path, metrics: List[Any]) -> None:
        CSVReporter._save_csv(
            output_path,
            metrics,
            empty_message="No metrics to save in {output_path}"
        )

    @staticmethod
    def save_red_flags(output_path: Path, changes: List[Any]) -> None:
        CSVReporter._save_csv(
            output_path,
            changes,
            empty_message="No red flags to save in {output_path}"
        )