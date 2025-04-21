# sqlite_adapter.py
import sys
import importlib

def patch_sqlite():
    """Force use of pysqlite3 with ChromaDB"""
    try:
        __import__('pysqlite3')
        sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
        importlib.invalidate_caches()
        return True
    except ImportError:
        return False

# Apply patch immediately
patch_success = patch_sqlite()