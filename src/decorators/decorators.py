# decorators.py

from functools import wraps
from sentence_transformers import SentenceTransformer
import faiss
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize Sentence Transformer model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Function to convert text to vector
def text_to_vector(text):
    return model.encode(text)

# Function to add vector to Faiss index
def add_to_vector_db(vector, metadata):
    # Placeholder for adding vector to Faiss index
    logging.info(f"Adding vector to DB with metadata: {metadata}")
    # Here you would add the vector to the Faiss index

# Updated decorator for any class
def index_for_vector_db(cls):
    # Extract docstring
    docstring = cls.__doc__ or ""
    
    # Extract public attributes
    attributes = [attr for attr in dir(cls) if not attr.startswith("_") and not callable(getattr(cls, attr))]
    
    # Extract methods
    methods = [func for func in dir(cls) if callable(getattr(cls, func)) and not func.startswith("_")]
    
    # Create metadata
    metadata = {
        "class_name": cls.__name__,
        "docstring": docstring,
        "attributes": attributes,
        "methods": methods
    }

    # Convert metadata to vector
    vector = text_to_vector(str(metadata))

    # Add vector to Faiss index
    add_to_vector_db(vector, metadata)
    logging.info(f"Class {cls.__name__} indexed with metadata: {metadata}")
    
    return cls

# Example usage for a generic class
@index_for_vector_db
class ExampleClass:
    """Example class for indexing"""
    attribute1 = "value1"
    attribute2 = "value2"
    
    def example_method(self):
        pass
