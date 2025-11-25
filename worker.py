from pathlib import Path
import time
import contextlib
from io import StringIO

from utils import synchronized_print, FileHandler
from analyzers import PackageAnalyzer
from reporters import *

def analyze_single_package(item):
    """Analyzing a single npm package with optional local versions"""
    package, out_dir, package_index, total_packages, include_local, local_dir = item
    pkg_dir = Path(out_dir) / package.replace('/', '_')
    FileHandler.ensure_directory(pkg_dir)

    start_time = time.time()
    synchronized_print(f"[{package_index}/{total_packages}] Analyzing {package}...")

    analyzer = PackageAnalyzer(include_local=include_local, local_versions_dir=local_dir)

    # File to save detailed output
    pkg_output_file = pkg_dir / f"{package.replace('/', '_')}.txt"

    # Capture the output of analyze_package
    output_buffer = StringIO()
    with contextlib.redirect_stdout(output_buffer):
        metrics, flags = analyzer.analyze_package(package)

    # Save the detailed output to the package file
    captured_output = output_buffer.getvalue()
    with open(pkg_output_file, 'w', encoding='utf-8') as f:
        f.write(f"=== Analysis of {package} ===\n")
        if include_local:
            f.write("Git versions + Local versions\n")
        else:
            f.write("Git versions only\n")
        f.write(captured_output)

    # Save the results
    metrics_file = pkg_dir / "all_metrics.csv"
    flags_file = pkg_dir / "red_flags.csv"
    summary_file = pkg_dir / "red_flags_summary.txt"

    CSVReporter().save_metrics(metrics_file, metrics)
    CSVReporter().save_red_flags(flags_file, flags)
    TextReporter().generate_summary(summary_file, flags)

    # Append save messages to the package file
    with open(pkg_output_file, 'a', encoding='utf-8') as f:
        f.write(f"Saved {len(metrics)} metrics in {metrics_file}\n")
        f.write(f"Saved {len(flags)} red flags in {flags_file}\n")
        f.write(f"Saved summary in {summary_file}\n")

    elapsed_time = time.time() - start_time
    synchronized_print(f"[{package_index}/{total_packages}] Completed: {package} -> {pkg_dir} ({elapsed_time:.1f}s)")

    return package