from abc import ABC, abstractmethod

class VectorDBInterface(ABC):
    @abstractmethod
    def add_vectors(self, vectors):
        pass

    @abstractmethod
    def remove_vector(self, idx):
        pass

    @abstractmethod
    def search(self, query_vector, k=5):
        pass
