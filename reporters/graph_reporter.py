import matplotlib.pyplot as plt
from pathlib import Path
from typing import List, Dict
from utils.logging_utils import synchronized_print
from models.graph_label import GraphLabel
import pandas as pd
from packaging.version import Version

class GraphReporter:
    """Generate evolution graphs for metrics across versions"""

    def normalize_version(v: str) -> Version:
        return Version(v.lstrip("v").replace("-local", ""))

    @staticmethod
    def generate_evolution_graphs(output_dir: Path, package_name: str) -> None:
        from analyzers import AggregateMetricsByTag

        """Generate graphs for all metrics grouped by class."""

        df = pd.read_csv(output_dir / "aggregate_metrics_by_tag.csv")
        if df.empty:
            print(f"No metrics to plot for {package_name}")
            return
        
        # Prepare data: versions and metrics
        #sorted_versions = sorted(df['version'].unique(), key=lambda v: list(map(int, v.split('.'))))
        sorted_versions = sorted(df['version'].unique(), key=GraphReporter.normalize_version)
        
        version_metrics = {}

        for _, row in df.iterrows():
            version = row['version']
            metrics_dict = row.to_dict()
            del metrics_dict['package']
            del metrics_dict['version']
            version_metrics[version] = metrics_dict

        # Create directory for graphs
        graphs_dir = output_dir / "graphs"
        graphs_dir.mkdir(exist_ok=True)
                
        # Generate graphs for each metric class
        for class_name, metric_names in AggregateMetricsByTag.METRIC_CLASSES.items():
            if class_name == 'OTHER_METRICS' or class_name == 'MAX_METRICS':
                GraphReporter._plot_individual(
                    graphs_dir,
                    sorted_versions,
                    version_metrics,
                    package_name
                )
            else:
                GraphReporter._plot_class_metrics(
                    graphs_dir, 
                    sorted_versions, 
                    version_metrics, 
                    metric_names, 
                    package_name, 
                    class_name
                )
    
    @staticmethod
    def _plot_class_metrics(graphs_dir: Path, versions: List[str], version_metrics: Dict, metric_names: List[str], package_name: str, class_name: str) -> None:
        """Generates a graph with all the metrics of a class"""
        
        metrics_data = {}
        for metric_name in metric_names:
            values = [version_metrics[v].get(metric_name, 0) for v in versions]
            # Skip non-numeric metrics (list[str])
            if not all(isinstance(v, (int, float)) for v in values):
                continue
            metrics_data[metric_name] = values
        
        # Create the graph
        plt.figure(figsize=(14, 8))
        
        # Plot each metric with a different color
        for idx, (metric_name, values) in enumerate(metrics_data.items()):
            color_idx = idx % len(GraphLabel.COLOR_PALETTE)
            plt.plot(
                range(len(versions)), 
                values, 
                marker='o', 
                linewidth=2, 
                markersize=6,
                color=GraphLabel.COLOR_PALETTE[color_idx],
                label=GraphLabel.METRIC_LABELS.get(metric_name, metric_name)
            )
        
        # Chart configuration
        plt.xlabel('Version', fontsize=12, fontweight='bold')
        plt.ylabel('Metric Value', fontsize=12, fontweight='bold')
        
        # Title
        class_title = GraphLabel.CLASS_TITLES.get(class_name, class_name)
        plt.title(f'{package_name} - {class_title}', fontsize=14, fontweight='bold')
        
        # Version labels
        plt.xticks(range(len(versions)), versions, rotation=45, ha='right')
        
        # Legend
        plt.legend(loc='best', fontsize=10, framealpha=0.9)
        
        # Grid
        plt.grid(True, alpha=0.3, linestyle='--')
        
        # Layout
        plt.tight_layout()
        
        # Save the graph
        output_file = graphs_dir / f"{class_name.lower()}_graph.png"
        plt.savefig(output_file, dpi=150, bbox_inches='tight')
        plt.close()


    @staticmethod
    def _plot_individual(graphs_dir: Path, versions: List[str], version_metrics: Dict, package_name: str) -> None:
        from analyzers import AggregateMetricsByTag

        """Generates individual graphs for each OTHER_METRICS metric."""
        other_metrics = AggregateMetricsByTag.METRIC_CLASSES.get('OTHER_METRICS', [])
        max_metrics = AggregateMetricsByTag.METRIC_CLASSES.get('MAX_METRICS', [])
        all_metrics = other_metrics + max_metrics

        for metric_name in all_metrics:
            values = [version_metrics[v].get(metric_name, 0) for v in versions]
            # Skip non-numeric metrics (list[str])
            if not all(isinstance(v, (int, float)) for v in values):
                continue

            plt.figure(figsize=(10, 6))
            plt.plot(
                range(len(versions)), 
                values, 
                marker='o', 
                linewidth=2, 
                markersize=6,
                color=GraphLabel.COLOR_PALETTE[0],
                label=GraphLabel.METRIC_LABELS.get(metric_name, metric_name)
            )
            
            plt.xlabel('Version', fontsize=12, fontweight='bold')
            plt.ylabel('Metric Value', fontsize=12, fontweight='bold')
            plt.title(f'{package_name} - {GraphLabel.METRIC_LABELS.get(metric_name, metric_name)} Evolution', fontsize=14, fontweight='bold')
            plt.xticks(range(len(versions)), versions, rotation=45, ha='right')
            plt.legend(loc='best', fontsize=10, framealpha=0.9)
            plt.grid(True, alpha=0.3, linestyle='--')
            plt.tight_layout()
            
            output_file = graphs_dir / f"{metric_name}_evolution.png"
            plt.savefig(output_file, dpi=150, bbox_inches='tight')
            plt.close()