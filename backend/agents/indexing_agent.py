from .vector_store import get_vector_store, save_vector_store, clear_vector_store

CLEAR_VECTOR_STORE_ON_UPLOAD = True

class IndexingAgent:

    def index(self, chunks):
        # Clear old vector store if flag is enabled
        if CLEAR_VECTOR_STORE_ON_UPLOAD:
            print("Clearing old vector store...")
            clear_vector_store()
            print("Old vector store cleared before indexing new document")
        else:
            print("Retaining existing vector store; new chunks will be added to it")

        store = get_vector_store()
        store.add_texts(chunks)
        save_vector_store(store)
