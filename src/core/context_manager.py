from sentence_transformers import SentenceTransformer
import numpy as np
import argparse
import os
import sys
import logging
from src.core.faiss_db import FaissDB

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Set UTF-8 encoding for standard output
sys.stdout.reconfigure(encoding='utf-8')

class ContextManager:
    def __init__(self, dimension=384, model_name='all-MiniLM-L6-v2', data_file='vector_db/states/data.txt'):
        self.model = SentenceTransformer(model_name)
        self.index = FaissDB(dimension)
        self.data_file = data_file
        self.data = []
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r', encoding='utf-8') as f:
                self.data = f.read().splitlines()

    def add_texts(self, texts):
        vectors = self.model.encode(texts)
        if len(vectors) > 0:
            self.index.add_vectors(np.array(vectors, dtype='float32'))
            logging.info(f"Data added to the Faiss index. Current index size: {self.get_index_size()}")
        else:
            logging.warning("No vectors were encoded. Please check the input data.")

    def search(self, query, k=20, index_file_path: str = "vector_db/states/index.faiss"):
        # Load the index from file
        self.load_index(index_file_path)
        query_vector = self.model.encode([query])
        if len(query_vector) > 0:
            distances, indices = self.index.search(np.array(query_vector, dtype='float32'), k)
            logging.info(f"Search query: '{query}' resulted in distances: {distances} and indices: {indices}")
            results = [self.data[i] for i in indices[0]]
            logging.info("Results:")
            for result in results:
                logging.info(result.encode('utf-8').decode('utf-8'))
            return results
        else:
            logging.warning("No query vector was encoded. Please check the input data.")

    def get_index_size(self):
        return self.index.index.ntotal

    def save_index(self, file_path):
        # Ensure the directory exists
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        self.index.save(file_path)
        logging.info(f"Index saved to {file_path}.")

    def load_index(self, file_path):
        self.index.load(file_path)
        logging.info(f"Index loaded from {file_path}. Current index size: {self.get_index_size()}")

    def save_metadata_to_file(self, metadata, file_path='vector_db/states/metadata.txt'):
        """Save metadata to a text file."""
        with open(file_path, 'a', encoding='utf-8') as f:
            f.write(f"{metadata}\n")
        logging.info(f"Metadata saved to {file_path}.")


# Add CLI functionality
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Vector Database CLI Tool')
    parser.add_argument('command', choices=['add_docs', 'search', "vector_size", "save_index", "load_index"], help='Command to execute')
    parser.add_argument('--file', type=str, help='Path to the documentation file to add or index file to save/load')
    parser.add_argument('--query', type=str, help='Search query')
    parser.add_argument('--k', type=int, default=20, help='Number of search results to return')
    args = parser.parse_args()

    context_manager = ContextManager()

    if args.command == 'add_docs' and args.file:
        # context_manager.add_full_documentation_to_index(args.file)
        logging.error("add_full_documentation_to_index method does not exist.")
    elif args.command == 'search' and args.query:
        results = context_manager.search(args.query, args.k)
        logging.info(f"Search results for '{args.query}':")
        for result in results:
            logging.info(result)
    elif args.command == 'vector_size':
        logging.info(f"Index size: {context_manager.get_index_size()}")
    elif args.command == 'save_index' and args.file:
        context_manager.save_index(args.file)
    elif args.command == 'load_index' and args.file:
        context_manager.load_index(args.file)
    else:
        parser.print_help()
