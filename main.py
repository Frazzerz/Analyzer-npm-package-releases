import argparse
from multiprocessing import cpu_count
import sys
from pathlib import Path
from datetime import datetime

from runner import run_tasks
from utils import TeeOutput, FileHandler

def main():
    parser = argparse.ArgumentParser(description='Analyzer npm package releases')
    parser.add_argument('--json', required=True)
    parser.add_argument('--output', default='analysis_results', help='Output directory (default: analysis_results)')
    parser.add_argument('--workers', type=int, default=cpu_count(), help=f'Number of workers (default: {cpu_count()})')
    parser.add_argument('--log', default='log.txt', help='Log file (default: log.txt)')
    parser.add_argument('--local', action='store_true', help='Include local versions from other_versions directory (default: False)')
    parser.add_argument('--local-dir', default='./other_versions', help='Directory for local versions (default: ./other_versions)')
    args = parser.parse_args()

    # setup log
    original_stdout = sys.stdout
    log_path = Path(args.log)
    FileHandler.ensure_directory(log_path.parent)
    log_file = TeeOutput(log_path)
    sys.stdout = log_file
    print(f"=== LOG ANALYSIS STARTED {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ===")

    try:
        packages = FileHandler.load_packages_from_json(args.json)
        if not packages:
            raise SystemExit("Error: No package in JSON file")

        print('=' * 50)
        print('NPM PACKAGE ANALYZER')
        print(f'Packages to analyze: {len(packages)}')
        print(f'Worker(s): {args.workers}')
        print(f'Output directory: {args.output}')
        print(f'Include local versions: {args.local}')
        if args.local:
            print(f'Local versions directory: {args.local_dir}')
        if args.log:
            print(f'Log: {args.log}')
        print('=' * 50)

        FileHandler.ensure_directory(Path(args.output))

        # Prepare tasks
        total_packages = len(packages)
        tasks = [(pkg, args.output, i+1, total_packages, args.local, args.local_dir) for i, pkg in enumerate(packages)]

        results, total_time = run_tasks(tasks, workers=args.workers)

        print('\n' + '=' * 50)
        print('ANALYSIS COMPLETED')
        print(f'Total time: {total_time:.1f}s')
        print(f'Packages analyzed: {len(results)}')
        print('=' * 50)

    finally:
        if args.log:
            print(f"=== LOG ANALYSIS ENDED {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ===")
            sys.stdout = original_stdout
            log_file.close()

if __name__ == '__main__':
    main()