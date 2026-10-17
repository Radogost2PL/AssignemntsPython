import functools
import time
from datetime import datetime
from pathlib import Path


import functools
import time
from datetime import datetime

import logging

logging.basicConfig(level=logging.DEBUG)

def log_time(func):
    def wrapper(*args, **kwargs):
        print(f"[{datetime.now():%H:%M:%S}] START metody: {func.__name__}")
        start = time.perf_counter()
        try:
            return func(*args, **kwargs)
        finally:
            elapsed = time.perf_counter() - start
            print(
                f"[{datetime.now():%H:%M:%S}] KONIEC metody: {func.__name__} "
                f"Czas wykonania: ({elapsed:.4f} s)"
            )
    return wrapper