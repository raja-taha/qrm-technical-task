import os
import shutil
from langchain_community.vectorstores import FAISS
from .langchain_embeddings import embeddings

VECTOR_DIR = "vector_store"

def clear_vector_store():
    """Delete the entire vector store directory"""
    if os.path.exists(VECTOR_DIR):
        shutil.rmtree(VECTOR_DIR)

def get_vector_store():
    if os.path.exists(os.path.join(VECTOR_DIR, "index.faiss")):
        return FAISS.load_local(
            VECTOR_DIR,
            embeddings,
            allow_dangerous_deserialization=True
        )
    # Create an empty FAISS store with a dummy text
    return FAISS.from_texts(["placeholder"], embeddings)

def save_vector_store(store):
    os.makedirs(VECTOR_DIR, exist_ok=True)
    store.save_local(VECTOR_DIR)