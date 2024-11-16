# test_decorators.py

import pytest
from src.decorators.decorators import index_for_vector_db, text_to_vector

@pytest.fixture
def mock_add_to_vector_db(mocker):
    mock_db = []

    def mock_function(vector, metadata):
        mock_db.append((vector, metadata))
        print("Mock add_to_vector_db called with:", metadata)

    mocker.patch('src.decorators.decorators.add_to_vector_db', new=mock_function)
    return mock_db


def test_index_for_vector_db(mock_add_to_vector_db):
    # Instantiate the class to trigger the decorator
    @index_for_vector_db
    class TestClass:
        """Test class for indexing"""
        attribute0 = "value1"
        attribute1 = "value2"

        def example_method(self):
            pass

    class_instance = TestClass()

    # Check if the class's metadata was added to the mock database
    assert len(mock_add_to_vector_db) == 1
    vector, metadata = mock_add_to_vector_db[0]

    assert metadata['class_name'] == 'TestClass'
    assert 'attribute0' in metadata['attributes']
    assert 'attribute1' in metadata['attributes']
    assert 'example_method' in metadata['methods']
    assert 'Test class for indexing' in metadata['docstring']

    # Check if the vector is not empty
    assert vector is not None
