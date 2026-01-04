from pathlib import Path
import pandas as pd

class TextReporter:
    """Generate flag text report considering all flag fields"""

    @staticmethod
    def generate_log_txt(pkg_dir: Path, package: str, output_buffer: str) -> None:
        """Generate log file with the captured output during analysis"""
        pkg_output_file = pkg_dir / f"{package.replace('/', '_')}.txt"
        captured_output = output_buffer.getvalue()

        with open(pkg_output_file, 'w', encoding='utf-8') as f:
            f.write(f"=== Analysis of {package} ===\n")
            f.write(captured_output)
    
    @staticmethod
    def generate_compact_report(output_dir: Path, package: str) -> None:
        """Compact report showing where each flag is active (from CSV)"""

        summary_file = output_dir / "flags_summary.txt"
        csv_file = output_dir / "flags.csv"
        try:
            df = pd.read_csv(csv_file)
        except FileNotFoundError:
            print(f"No flags.csv found for {package}, skipping report generation.")
            return
        if df.empty:
            print(f"No metrics to plot for {package}")
            return

        # collumns that are not flags
        non_flag_cols = {"package", "version_from", "version_to"}

        flag_columns = [c for c in df.columns if c not in non_flag_cols]

        with open(summary_file, "w", encoding="utf-8") as f:
            f.write(f"FLAGS REPORT - Package: {package}\n")
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
                f.write("No flags detected in any version\n")