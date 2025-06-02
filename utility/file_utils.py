import os
import json


def save_dict_to_file(data: dict, relative_path: str, base_dir: str = 'assets', ensure_dir: bool = True,
                      indent: int = 4, encoding: str = 'utf-8'):
    """
    将字典数据保存为 JSON 文件，路径基于 base_dir（默认 'assets'）。

    参数:
        data (dict): 要保存的字典数据。
        relative_path (str): 相对于 base_dir 的路径，如 'configs/settings.json'。
        base_dir (str): 基础目录，默认是 'assets'。
        ensure_dir (bool): 如果路径不存在，是否创建目录（默认 True）。
        indent (int): JSON 缩进格式，默认 4。
        encoding (str): 文件编码，默认 utf-8。

    示例:
        save_dict_to_file({'a': 1}, 'configs/config.json')
        # 保存到 assets/configs/config.json
    """
    full_path = os.path.join(base_dir, relative_path)

    if ensure_dir:
        os.makedirs(os.path.dirname(full_path), exist_ok=True)

    with open(full_path, 'w', encoding=encoding) as f:
        json.dump(data, f, indent=indent, ensure_ascii=False)


def load_dict_from_file(relative_path: str, base_dir: str = 'assets', encoding: str = 'utf-8') -> dict:
    """
    从 JSON 文件加载字典数据，路径基于 base_dir（默认 'assets'）。

    参数:
        relative_path (str): 相对于 base_dir 的路径，例如 'config/settings.json'。
        base_dir (str): 基础路径，默认 'assets'。
        encoding (str): 文件编码，默认 'utf-8'。

    返回:
        dict: 加载的 JSON 数据。

    异常:
        FileNotFoundError: 如果文件不存在。
        json.JSONDecodeError: 如果文件内容不是合法 JSON。
    """
    full_path = os.path.join(base_dir, relative_path)

    with open(full_path, 'r', encoding=encoding) as f:
        return json.load(f)
