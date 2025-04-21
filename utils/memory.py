# utils/memory.py
import gc
import psutil
import torch

def memory_guard():
    """Check memory usage and clean up"""
    mem = psutil.virtual_memory()
    if mem.percent > 80:
        gc.collect()
        torch.cuda.empty_cache() if torch.cuda.is_available() else None
        return True
    return False

def log_memory():
    """Debug memory usage"""
    process = psutil.Process()
    return f"{process.memory_info().rss / 1024 ** 2:.1f}MB used"