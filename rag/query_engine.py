from vector_store import get_chroma_client
from llama_index.vector_stores.chroma import ChromaVectorStore

def get_rag_engine():
    client = get_chroma_client()
    collection = client.get_or_create_collection("manifestation_knowledge")

from llama_index.llms.huggingface import HuggingFaceLLM
from llama_index.core import Settings, VectorStoreIndex, ServiceContext
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core import StorageContext
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
import torch
import os
# Add this at the beginning of the file (line 2 or 3)
import chromadb

os.environ["TOKENIZERS_PARALLELISM"] = "false"

from database import get_chroma_client  # Instead of direct chromadb import




def get_rag_engine():
    # Initialize LLM with proper parenthesis matching
    llm = HuggingFaceLLM(
        model_name="TinyLlama/TinyLlama-1.1B-Chat-v1.0",
        tokenizer_name="TinyLlama/TinyLlama-1.1B-Chat-v1.0",
        device_map="cpu",
        model_kwargs={
            "torch_dtype": torch.float32,
            "low_cpu_mem_usage": True,
            "offload_folder": "./offload"
        },  # This comma was likely missing
        generate_kwargs={
            "temperature": 0.7,
            "max_new_tokens": 150
        }
    )
    
    # Rest of your implementation...
      # Lighter embedding model - MUST CHANGE THIS
    embed_model = HuggingFaceEmbedding(
        model_name="sentence-transformers/all-MiniLM-L6-v2",  # 22MB model
        device="cpu"
    )
    
    # Initialize ChromaDB with persistent storage
    chroma_client = chromadb.PersistentClient(path="./chroma_db")
    vector_store = ChromaVectorStore(
        chroma_collection=chroma_client.get_or_create_collection(
            "manifestation_knowledge",
            metadata={"hnsw:space": "cosine"}  # Optimized similarity metric
        )
    )
    
    # Configure global settings
    Settings.embed_model = embed_model
    Settings.llm = llm
    Settings.chunk_size = 1024  # Optimal for Mistral's context window
    
    # Create and return query engine
    index = VectorStoreIndex.from_vector_store(
        vector_store=vector_store,
    )
    
    return index.as_query_engine(
        similarity_top_k=3,
        response_mode="compact",  # Balances conciseness and completeness
        verbose=True  # For debugging
    )