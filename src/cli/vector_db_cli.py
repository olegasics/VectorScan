import ast
import os
import logging
from src.core.context_manager import ContextManager
import click

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

@click.group()
def cli():
    """Vector Database CLI"""
    logging.info("CLI initialized.")
    pass

def get_python_files(directory):
    """Retrieve all Python files in the directory."""
    python_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                python_files.append(os.path.join(root, file))
    return python_files


def analyze_class_decorators(file_path):
    """Analyze classes in a file and check for the specific decorator."""
    with open(file_path, 'r', encoding='utf-8') as f:
        source = f.read()
        tree = ast.parse(source)
        classes_with_decorator = []
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                for decorator in node.decorator_list:
                    if isinstance(decorator, ast.Name) and decorator.id == 'index_for_vector_db':
                        classes_with_decorator.append(node)
        return classes_with_decorator


def extract_metadata(node):
    """Extract metadata from a class node."""
    class_name = node.name
    docstring = ast.get_docstring(node)
    attributes = [n.targets[0].id for n in node.body if isinstance(n, ast.Assign)]
    methods = [n.name for n in node.body if isinstance(n, ast.FunctionDef)]
    return {
        "class_name": class_name,
        "docstring": docstring,
        "attributes": attributes,
        "methods": methods
    }


@cli.command()
@click.argument('directory', type=click.Path(exists=True))
def scan_and_index(directory):
    """Scan the project for classes with the decorator and index them."""
    logging.info(f"Scanning directory: {directory}")
    context_manager = ContextManager()
    python_files = get_python_files(directory)
    for file_path in python_files:
        logging.info(f"Scanning file: {file_path}")
        classes_with_decorator = analyze_class_decorators(file_path)
        for node in classes_with_decorator:
            metadata = extract_metadata(node)
            context_manager.save_metadata_to_file(metadata)
            logging.info(f"Indexed class: {metadata['class_name']} from {file_path}")

if __name__ == '__main__':
    cli()