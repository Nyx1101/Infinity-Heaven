import os
import json


def save_dict_to_file(
    data: dict,
    relative_path: str,
    base_dir: str = 'assets',
    ensure_dir: bool = True,
    indent: int = 4,
    encoding: str = 'utf-8'
):
    """
    Save a dictionary to a JSON file.
    This function ensures the directory exists (if specified), and writes the dictionary
    to the given path in JSON format with optional indentation and encoding.
    """
    # Construct the full file path
    full_path = os.path.join(base_dir, relative_path)

    # Create the directory if it does not exist
    if ensure_dir:
        os.makedirs(os.path.dirname(full_path), exist_ok=True)

    # Write the dictionary to the file as JSON
    with open(full_path, 'w', encoding=encoding) as f:
        json.dump(data, f, indent=indent, ensure_ascii=False)


def load_dict_from_file(
    relative_path: str,
    base_dir: str = 'assets',
    encoding: str = 'utf-8'
) -> dict:
    """
    Load a dictionary from a JSON file.
    This function reads the JSON file from the given path and parses it into a Python dictionary.
    """
    # Construct the full file path
    full_path = os.path.join(base_dir, relative_path)

    # Read and parse the JSON file
    with open(full_path, 'r', encoding=encoding) as f:
        return json.load(f)