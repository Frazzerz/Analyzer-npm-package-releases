import matplotlib.pyplot as plt
from pathlib import Path
import pandas as pd
from models import GraphLabel
from matplotlib.ticker import MaxNLocator

class GraphReporter:

    @staticmethod
    def generate_graphs(output_dir: Path, package_name: str) -> None:
        """Generate one graph per metric"""

        metrics_file = output_dir / "aggregate_metrics_by_tag.csv"
        history_file = output_dir / "aggregate_metrics_history.csv"

        if not metrics_file.exists() and not history_file.exists():
            print(f"No metrics to plot for {package_name}")
            return

        graphs_dir = output_dir / "graphs"
        graphs_dir.mkdir(exist_ok=True)

        version_metric_cols = set()
        aggregate_metric_cols = set()

        for category in GraphLabel.METRICS.values():
            for vm_key, (avg_key, _) in category["metrics"].items():
                version_metric_cols.add(vm_key)
                aggregate_metric_cols.add(avg_key)

        df = pd.read_csv(metrics_file,usecols=["version", *version_metric_cols])
        df_history = pd.read_csv(history_file,usecols=list(aggregate_metric_cols))

        if df.empty and df_history.empty:
            print(f"No metrics to plot for {package_name}")
            return

        # versions already ordered in CSV
        versions = df["version"].tolist()

        # generate graphs
        for category in GraphLabel.METRICS.values():
            for metric_key, (metric_key_hist, label) in category["metrics"].items():

                values = (df[metric_key].tolist())
                history_values = (df_history[metric_key_hist].tolist())

                # plot
                plt.figure(figsize=(10, 5))

                plt.plot(
                    versions,
                    values,
                    marker="o",
                    linewidth=2,
                    color="blue",
                    label="Single version"
                )

                plt.plot(
                    versions,
                    history_values,
                    linestyle="--",
                    linewidth=2,
                    color="red",
                    label="Aggregate versions (avg)"
                )

                plt.title(f"{label} - {package_name}")
                plt.xlabel("Version")
                plt.ylabel(label)
                # set x axis to have a maximum of 12 ticks
                if len(versions) > 12:
                    ax = plt.gca()
                    ax.xaxis.set_major_locator(MaxNLocator(nbins=12))
                plt.xticks(rotation=45)
                plt.grid(True)
                plt.legend()
                plt.tight_layout()

                output_path = graphs_dir / f"{metric_key}.png"
                plt.savefig(output_path)
                plt.close()
        
        print(f"Generated graphs for {package_name} in {graphs_dir}")