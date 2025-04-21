# FIRST LINE in api/main.py
# FIRST LINE - must come before any chromadb imports
import sqlite_adapter  # Your existing SQLite patcher

# Then import ChromaDB components

import patch_sqlite  # Must come before chromadb imports

# Rest of your existing imports...
from fastapi import FastAPI
from pydantic import BaseModel
# ...
from fastapi import FastAPI
from pydantic import BaseModel
from contextlib import asynccontextmanager
from typing import Optional
from utils.memory import memory_guard, log_memory

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from pathlib import Path

app = FastAPI(title="Manifestation Coach API")

# Add root endpoint
@app.get("/", response_class=HTMLResponse)
async def root():
    return """
    <html>
        <head>
            <title>Manifestation Coach API</title>
        </head>
        <body>
            <h1>Manifestation Coach API</h1>
            <p>Available endpoints:</p>
            <ul>
                <li><a href="/docs">/docs</a> - Interactive API docs</li>
                <li>POST /query - Submit your manifestation questions</li>
            </ul>
        </body>
    </html>
    """

# Add favicon endpoint to prevent 404 errors
@app.get("/favicon.ico")
async def favicon():
    return FileResponse(Path(".") / "favicon.ico")  # Optional: add a favicon.ico file

    
# Modern lifespan management
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    try:
        from rag.query_engine import get_rag_engine
        app.state.engine = get_rag_engine()
        print("Startup complete. Memory:", log_memory())
        yield
    except ImportError as e:
        print(f"Startup failed: {str(e)}")
        raise

app = FastAPI(title="Manifestation Coach API", lifespan=lifespan)

class Query(BaseModel):
    text: str
    user_id: Optional[str] = None

@app.post("/query")
async def process_query(query: Query):
    if memory_guard():
        print("Warning: High memory usage detected")
    try:
        response = app.state.engine.query(query.text)
        return {
            "answer": str(response),
            "memory": log_memory(),
            "sources": [node.node.metadata for node in response.source_nodes]
        }
    except Exception as e:
        return {"error": str(e), "memory": log_memory()}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)