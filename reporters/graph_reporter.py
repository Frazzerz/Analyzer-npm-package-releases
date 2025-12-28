import matplotlib.pyplot as plt
from pathlib import Path
import pandas as pd
from packaging.version import Version
from models import GraphLabel

class GraphReporter:
    """Generate evolution graphs for metrics across versions"""

    @staticmethod
    def normalize_version(v: str) -> Version:
        return Version(v.lstrip("v").replace("-local", ""))

    @staticmethod
    def generate_evolution_graphs(output_dir: Path, package_name: str) -> None:
        """Generate one graph per metric"""

        df = pd.read_csv(output_dir / "aggregate_metrics_by_tag.csv")
        if df.empty:
            print(f"No metrics to plot for {package_name}")
            return

        sorted_versions = sorted(df['version'].unique(),key=GraphReporter.normalize_version)

        graphs_dir = output_dir / "graphs"
        graphs_dir.mkdir(exist_ok=True)
        color_cycle = iter(GraphLabel.COLOR_PALETTE)

        # Iterate over ALL metrics defined in GraphLabel
        for category in GraphLabel.METRICS.values():
            for metric_key, metric_label in category["metrics"].items():

                if metric_key not in df.columns:
                    continue  # metric not present in CSV

                values = []
                for version in sorted_versions:
                    row = df[df["version"] == version]
                    if row.empty:
                        values.append(0)
                    else:
                        values.append(row.iloc[0][metric_key])

                plt.figure(figsize=(10, 5))
                plt.plot(
                    sorted_versions,
                    values,
                    marker="o",
                    color=next(color_cycle, None),
                    linewidth=2
                )

                plt.title(f"{metric_label} – {package_name}")
                plt.xlabel("Version")
                plt.ylabel(metric_label)
                plt.xticks(rotation=45)
                plt.grid(True)
                plt.tight_layout()

                output_path = graphs_dir / f"{metric_key}.png"
                plt.savefig(output_path)
                plt.close()

                #print(f"Saved graph: {output_path}")
        
        print(f"Generated graphs for {package_name} in {graphs_dir}")