import os
import json


def save_dict_to_file(data: dict, relative_path: str, base_dir: str = 'assets', ensure_dir: bool = True,
                      indent: int = 4, encoding: str = 'utf-8'):
    full_path = os.path.join(base_dir, relative_path)

    if ensure_dir:
        os.makedirs(os.path.dirname(full_path), exist_ok=True)

    with open(full_path, 'w', encoding=encoding) as f:
        json.dump(data, f, indent=indent, ensure_ascii=False)


def load_dict_from_file(relative_path: str, base_dir: str = 'assets', encoding: str = 'utf-8') -> dict:
    full_path = os.path.join(base_dir, relative_path)

    with open(full_path, 'r', encoding=encoding) as f:
        return json.load(f)
