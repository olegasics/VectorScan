import faiss
from src.core.base import VectorDBInterface

class FaissDB(VectorDBInterface):
    def __init__(self, dimension):
        self.index = faiss.IndexFlatL2(dimension)

    def add_vectors(self, vectors):
        self.index.add(vectors)

    def remove_vector(self, idx):
        # Faiss does not support direct removal, requires rebuilding index
        pass

    def search(self, query_vector, k=5):
        distances, indices = self.index.search(query_vector, k)
        return distances, indices
