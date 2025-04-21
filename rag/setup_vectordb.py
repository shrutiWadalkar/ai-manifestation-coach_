from llama_index import VectorStoreIndex, SimpleDirectoryReader
from llama_index.vector_stores import ChromaVectorStore
from llama_index.storage.storage_context import StorageContext
import chromadb

def setup_vector_db(data_dir="data/pdfs", persist_dir="./chroma_db"):
    # Load documents (PDFs, videos transcripts)
    documents = SimpleDirectoryReader(data_dir).load_data()
    
    # Initialize ChromaDB
    chroma_client = chromadb.PersistentClient(path=persist_dir)
    chroma_collection = chroma_client.create_collection("coach_knowledge")
    
    # Create vector store
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    
    # Build index
    index = VectorStoreIndex.from_documents(
        documents,
        storage_context=storage_context
    )
    
    return index