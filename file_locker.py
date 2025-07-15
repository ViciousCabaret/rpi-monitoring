import fcntl
import os


class LockException(Exception):
    pass


class ProcessLock:
    def __init__(self, lock_file_path: str):
        self.lock_file_path = lock_file_path
        self._lock_file = None

    def __enter__(self):
        pid = os.getpid()
        self._lock_file = open(self.lock_file_path, 'w')

        try:
            fcntl.flock(self._lock_file, fcntl.LOCK_EX | fcntl.LOCK_NB)
            # print(f"[{pid}] Uzyskano blokadę: {self.lock_file_path}")
        except (IOError, BlockingIOError):
            self._lock_file.close()
            raise LockException(f"[{pid}] Proces jest już uruchomiony (blokada na {self.lock_file_path}).")

    def __exit__(self, exc_type, exc_val, exc_tb):
        pid = os.getpid()
        if self._lock_file:
            fcntl.flock(self._lock_file, fcntl.LOCK_UN)
            self._lock_file.close()
            # print(f"[{pid}] Zwolniono blokadę: {self.lock_file_path}")