import csv
from pathlib import Path
from typing import List, Any, Dict
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
    
    @staticmethod
    def save_aggregate_metrics(output_path: Path, aggregate_metrics: Dict[str, Dict[str, int]], package: str) -> None:
        """Save aggregate metrics dictionary to CSV"""
        if not aggregate_metrics:
            print(f"No aggregate metrics to save in {output_path}")
            return
        
        # Convert the nested dictionary to a list of flat dictionaries
        rows = []
        for version, metrics in aggregate_metrics.items():
            row = {
                'package': package,
                'version': version
            }
            row.update(metrics)
            rows.append(row)
        
        if not rows:
            print(f"No aggregate metrics to save in {output_path}")
            return
        
        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            # Get fieldnames from the first row
            fieldnames = rows[0].keys()
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)