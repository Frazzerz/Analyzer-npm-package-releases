from pathlib import Path
from typing import List
from dataclasses import asdict, fields
from collections import defaultdict
from models import RedFlag
import pandas as pd

class TextReporter:
    """Generate red flag text report considering all red flag fields"""

    @staticmethod
    def generate_compact_report(output_dir: Path, package: str) -> None:
        """Compact report showing where each red flag is active (from CSV)"""

        summary_file = output_dir / "red_flags_summary.txt"
        csv_file = output_dir / "red_flags.csv"

        df = pd.read_csv(csv_file)

        if df.empty:
            print(f"No metrics to plot for {package}")
            return

        # collumns that are not red flags
        non_flag_cols = {"package", "version_from", "version_to"}

        flag_columns = [c for c in df.columns if c not in non_flag_cols]

        with open(summary_file, "w", encoding="utf-8") as f:
            f.write(f"RED FLAGS REPORT - Package: {package}\n")
            f.write("=" * 60 + "\n\n")

            any_flag = False

            for _, row in df.iterrows():
                version_key = f"{row['version_from']} → {row['version_to']}"

                active_flags = [
                    flag for flag in flag_columns
                    if bool(row[flag])
                ]

                if active_flags:
                    any_flag = True
                    f.write(f"{version_key}:\n")
                    for flag in active_flags:
                        f.write(f"  • {flag}\n")
                    f.write("\n")

            if not any_flag:
                f.write("No red flags detected in any version\n")