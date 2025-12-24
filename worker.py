from pathlib import Path
import time
import contextlib
from io import StringIO
from utils import FileHandler
from analyzers import PackageAnalyzer
from reporters import TextReporter, GraphReporter

def analyze_single_package(package, out_dir, package_index, total_packages, include_local, local_dir, workers):
    """Analyzing a single npm package with optional local versions"""
    pkg_dir = Path(out_dir) / package.replace('/', '_')
    FileHandler.ensure_directory(pkg_dir)

    start_time = time.time()
    print(f"[{package_index}/{total_packages}] Analyzing {package}...")

    analyzer = PackageAnalyzer(include_local=include_local, local_versions_dir=local_dir, workers=workers)

    # Capture the output of analyze_package
    output_buffer = StringIO()
    with contextlib.redirect_stdout(output_buffer):
        analyzer.analyze_package(package, pkg_dir)
    
    # Log file
    pkg_output_file = pkg_dir / f"{package.replace('/', '_')}.txt"
    captured_output = output_buffer.getvalue()
    with open(pkg_output_file, 'w', encoding='utf-8') as f:
        f.write(f"=== Analysis of {package} ===\n")
        if include_local:
            f.write("Git versions + Local versions\n")
        else:
            f.write("Git versions only\n")
        f.write(captured_output)

    # Text reports and graph
    TextReporter().generate_compact_report(pkg_dir, package)
    GraphReporter().generate_evolution_graphs(pkg_dir, package)

    elapsed_time = time.time() - start_time
    print(f"[{package_index}/{total_packages}] Completed: {package} -> {pkg_dir} ({elapsed_time:.1f}s)")

    return package