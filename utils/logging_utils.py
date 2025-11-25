import sys
from multiprocessing import Lock

# Lock to synchronize prints between processes
print_lock = Lock()

class TeeOutput:
    """Writes simultaneously to stdout and to a file"""
    def __init__(self, log_file):
        self.terminal = sys.stdout
        self.log_file = open(log_file, 'w', encoding='utf-8')

    def write(self, message):
        self.terminal.write(message)
        self.log_file.write(message)

    def flush(self):
        self.terminal.flush()
        self.log_file.flush()

    def close(self):
        try:
            self.log_file.close()
        except Exception:
            pass

def synchronized_print(*args, **kwargs):
    """Atomic and synchronized print to avoid mixing output between processes"""
    with print_lock:
        print(*args, **kwargs)

def setup_logging(log_file: str = "log.txt"):
    """Setup logging to both console and file"""
    tee = TeeOutput(log_file)
    sys.stdout = tee
    return tee