import time
from multiprocessing import Pool

from utils import synchronized_print

def run_tasks(tasks, workers):
    """Coordinator who is responsible for starting multiple processes and distributing tasks. Multiprocessing logic"""
    "No more needed"
    start_time = time.time()
    results = []
    synchronized_print(f"Starting processing with {workers} worker(s)...")

    with Pool(workers) as pool:                                 # How many workers to start
        for res in pool.imap_unordered(_wrap_task, tasks):      # Iterate on worker results
            results.append(res)

    total_time = time.time() - start_time
    return results, total_time


def _wrap_task(task):
    # to dynamically load worker.py inside processes (avoiding circular imports)
    from worker import analyze_single_package
    return analyze_single_package(task)