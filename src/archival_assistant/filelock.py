import os
from pathlib import Path
from datetime import datetime
import functools


class FileLockExistsException(Exception):
    def __init__(self, message, file_lock_object):
        super().__init__(message)
        self.lock_path = file_lock_object.lock_path
        self.created_by = file_lock_object.created_by
        self.created_on = file_lock_object.created_on


class FileLock:
    def __init__(self, lock_path: Path):
        self.lock_path = lock_path
        self.created_by = None
        self.created_on = None

    def _create_lock(self):
        self.created_by = os.getlogin()
        self.created_on = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
        with open(self.lock_path, 'w') as f:
            f.write(f'{self.created_by}\n{self.created_on}')

    def _lock_exists(self):
        if self.lock_path.exists():
            with open(self.lock_path, 'r') as f:
                self.created_by = f.readline().strip()
                self.created_on = f.readline().strip()
            return True
        return False

    def __enter__(self):
        if self._lock_exists():
            raise FileLockExistsException(f'Locked by {self.created_by} at {self.created_on}', self)
        else:
            self._create_lock()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.lock_path.unlink()

    @staticmethod
    def lock(lock_path):
        def decorating(func):
            @functools.wraps(func)
            def wrapper():
                with FileLock(lock_path):
                    func()
            return wrapper
        return decorating
