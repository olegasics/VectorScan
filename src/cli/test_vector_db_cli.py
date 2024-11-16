import pytest
import os
import ast
from src.cli.vector_db_cli import get_python_files, analyze_class_decorators, extract_metadata


def test_get_python_files(tmp_path):
    # Setup
    (tmp_path / "test1.py").write_text("# test file 1")
    (tmp_path / "test2.py").write_text("# test file 2")
    (tmp_path / "test.txt").write_text("# not a python file")

    # Execute
    python_files = get_python_files(tmp_path)

    # Verify
    assert len(python_files) == 2
    assert os.path.join(tmp_path, "test1.py") in python_files
    assert os.path.join(tmp_path, "test2.py") in python_files


def test_analyze_class_decorators(tmp_path):
    # Setup
    code = '''@index_for_vector_db
class TestClass:
    pass

class AnotherClass:
    pass
'''
    file_path = tmp_path / "test.py"
    file_path.write_text(code)

    # Execute
    classes_with_decorator = analyze_class_decorators(file_path)

    # Verify
    assert len(classes_with_decorator) == 1
    assert classes_with_decorator[0].name == "TestClass"


def test_extract_metadata():
    # Setup
    code = '''class TestClass:
    """Test docstring"""
    attribute1 = "value1"

    def method1(self):
        pass
'''
    tree = ast.parse(code)
    class_node = next(node for node in ast.walk(tree) if isinstance(node, ast.ClassDef))

    # Execute
    metadata = extract_metadata(class_node)

    # Verify
    assert metadata['class_name'] == "TestClass"
    assert metadata['docstring'] == "Test docstring"
    assert "attribute1" in metadata['attributes']
    assert "method1" in metadata['methods']
