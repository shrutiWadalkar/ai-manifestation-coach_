import numpy as np  # Now using compatible version
import chromadb
from chromadb.config import Settings
import os

def get_chroma_client():
    """Create a SQLite-free ChromaDB client"""
    return chromadb.Client(
        settings=Settings(
            chroma_db_impl="duckdb+parquet",
            persist_directory=os.path.join(os.getcwd(), "vector_data"),
            anonymized_telemetry=False
        )
    )
