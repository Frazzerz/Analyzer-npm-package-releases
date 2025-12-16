import matplotlib.pyplot as plt
from pathlib import Path
from typing import List, Dict
from utils import AggregateMetricsByTag

class GraphReporter:
    """Generate evolution graphs for metrics across versions"""
    
    METRIC_LABELS = {
        'suspicious_patterns_count': 'Suspicious Patterns',
        'longest_line_length': 'Longest Line Length',
        'platform_detections_count': 'Platform Detections',
        'timing_delays_count': 'Timing Delays',
        'eval_count': 'Eval Calls',
        'shell_commands_count': 'Shell Commands',
        'file_size_bytes': 'File Size (bytes)',
        'scan_functions_count': 'Scan Functions',
        'sensitive_elements_count': 'Sensitive Elements',
        'crypto_addresses': 'Crypto Addresses',
        'cryptocurrency_name': 'Cryptocurrency Names',
        'wallet_detection': 'Wallet Detections',
        'replaced_crypto_addresses': 'Replaced Addresses',
        'hook_provider': 'Hook Provider',
        'npm_maintainers': 'NPM Maintainers'
    }
    
    # Titles for each class
    CLASS_TITLES = {
        'EVASION_TECHNIQUES': 'Evasion Techniques Metrics',
        'PAYLOAD_DELIVERY_EXECUTION': 'Payload Delivery & Execution Metrics',
        'DATA_EXFILTRATION_C2': 'Data Exfiltration & C2 Metrics',
        'CRYPTOJACKING_WALLET_THEFT': 'Cryptojacking & Wallet Theft Metrics',
        'ACCOUNT_COMPROMISE': 'Account Compromise & Integrity Anomalies'
    }
    
    # Colors for lines (cycled for many metrics)
    COLOR_PALETTE = [
        '#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd',
        '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf',
        '#1a55FF', '#FF5733', '#33FF57', '#FF33F6', '#33FFF6'
    ]
    
    @staticmethod
    def generate_evolution_graphs(output_dir: Path, version_metrics: Dict[str, Dict[str, int]], package_name: str) -> None:
        """Generate graphs for all metrics grouped by class."""
        if not version_metrics:
            print(f"No metrics to plot for {package_name}")
            return
        
        # Versions are already sorted by aggregate_metrics_by_version
        sorted_versions = list(version_metrics.keys())
        
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
    def _plot_class_metrics(graphs_dir: Path, versions: List[str], 
                           version_metrics: Dict, metric_names: List[str], 
                           package_name: str, class_name: str) -> None:
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
            color_idx = idx % len(GraphReporter.COLOR_PALETTE)
            plt.plot(
                range(len(versions)), 
                values, 
                marker='o', 
                linewidth=2, 
                markersize=6,
                color=GraphReporter.COLOR_PALETTE[color_idx],
                label=GraphReporter.METRIC_LABELS.get(metric_name, metric_name)
            )
        
        # Chart configuration
        plt.xlabel('Version', fontsize=12, fontweight='bold')
        plt.ylabel('Metric Value', fontsize=12, fontweight='bold')
        
        # Title
        class_title = GraphReporter.CLASS_TITLES.get(class_name, class_name)
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
        output_file = graphs_dir / f"{class_name.lower()}_evolution.png"
        plt.savefig(output_file, dpi=150, bbox_inches='tight')
        plt.close()
        
        # Also generate a normalized graph for comparison
        GraphReporter._plot_normalized_class_metrics(
            graphs_dir, versions, metrics_data, metric_names, 
            package_name, class_name
        )
    
    @staticmethod
    def _plot_normalized_class_metrics(graphs_dir: Path, versions: List[str], 
                                      metrics_data: Dict, metric_names: List[str], 
                                      package_name: str, class_name: str) -> None:
        """Generates a normalized (0-1) graph to compare metrics on different scales."""
        # Normalize data for each metric
        normalized_data = {}
        for metric_name, values in metrics_data.items():
            if max(values) > 0:
                normalized = [v / max(values) for v in values]
            else:
                normalized = [0] * len(values)
            normalized_data[metric_name] = normalized
        
        plt.figure(figsize=(14, 8))
        
        for idx, (metric_name, values) in enumerate(normalized_data.items()):
            color_idx = idx % len(GraphReporter.COLOR_PALETTE)
            plt.plot(
                range(len(versions)), 
                values, 
                marker='o', 
                linewidth=2, 
                markersize=6,
                color=GraphReporter.COLOR_PALETTE[color_idx],
                label=GraphReporter.METRIC_LABELS.get(metric_name, metric_name)
            )
        
        plt.xlabel('Version', fontsize=12, fontweight='bold')
        plt.ylabel('Normalized Value (0-1)', fontsize=12, fontweight='bold')
        
        class_title = GraphReporter.CLASS_TITLES.get(class_name, class_name)
        plt.title(f'{package_name} - {class_title} (Normalized)', fontsize=14, fontweight='bold')
        
        plt.xticks(range(len(versions)), versions, rotation=45, ha='right')
        plt.legend(loc='best', fontsize=10, framealpha=0.9)
        plt.grid(True, alpha=0.3, linestyle='--')
        plt.tight_layout()

        output_file = graphs_dir / f"{class_name.lower()}_normalized.png"
        plt.savefig(output_file, dpi=150, bbox_inches='tight')
        plt.close()
    
    @staticmethod
    def _plot_individual(graphs_dir: Path, versions: List[str], 
                         version_metrics: Dict, package_name: str) -> None:
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
                color=GraphReporter.COLOR_PALETTE[0],
                label=GraphReporter.METRIC_LABELS.get(metric_name, metric_name)
            )
            
            plt.xlabel('Version', fontsize=12, fontweight='bold')
            plt.ylabel('Metric Value', fontsize=12, fontweight='bold')
            plt.title(f'{package_name} - {GraphReporter.METRIC_LABELS.get(metric_name, metric_name)} Evolution', fontsize=14, fontweight='bold')
            plt.xticks(range(len(versions)), versions, rotation=45, ha='right')
            plt.legend(loc='best', fontsize=10, framealpha=0.9)
            plt.grid(True, alpha=0.3, linestyle='--')
            plt.tight_layout()
            
            output_file = graphs_dir / f"{metric_name}_evolution.png"
            plt.savefig(output_file, dpi=150, bbox_inches='tight')
            plt.close()