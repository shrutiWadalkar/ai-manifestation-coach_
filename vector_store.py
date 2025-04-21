# vector_store.py
import os
import numpy as np
# Apply NumPy compatibility patches
np.float_ = np.float64
np.int_ = np.int64
np.uint = np.uint64

import chromadb
from chromadb.config import Settings

class VectorStore:
    def __init__(self):
        self.client = chromadb.Client(
            settings=Settings(
                chroma_db_impl="duckdb+parquet",
                persist_directory=os.path.join(os.getcwd(), "vector_data"),
                anonymized_telemetry=False
            )
        )
    
    def get_collection(self, name="knowledge"):
        return self.client.get_or_create_collection(name)

# Global instance
vector_store = VectorStore()