import xml.etree.ElementTree as ET
import base64

def load_vfs_from_xml(path):
    # загружает VFS из XML в структуру вложенных словарей.
    tree = ET.parse(path)
    root = tree.getroot()
    return _parse_xml_node(root)

def _parse_xml_node(element):
    result = {}
    for child in element:
        if child.tag == 'dir':
            name = child.get('name')
            if name:
                result[name] = _parse_xml_node(child)
        elif child.tag == 'file':
            name = child.get('name')
            data_b64 = child.text or ''
            try:
                result[name] = base64.b64decode(data_b64)
            except Exception:
                result[name] = b''
    return result

def create_default_vfs():
    # VFS по умолчанию (в памяти, ≥3 уровня).
    return {
        "home": {
            "user": {
                "docs": {
                    "notes.txt": b"Important note!"
                }
            }
        },
        "etc": {
            "motd": b"Welcome to Emulator VFS"
        }
    }

def get_node(vfs, path_parts):
     # возвращает узел по списку частей пути (без обработки . и ..)
    node = vfs
    for part in path_parts:
        if part == '':
            continue
        if not isinstance(node, dict) or part not in node:
            raise FileNotFoundError(f"No such file or directory")
        node = node[part]
        if isinstance(node, bytes) and len(path_parts) > 1:
            raise NotADirectoryError(f"Not a directory")
    return node

def normalize_path(current: str, target: str) -> list:
    # нормализует путь как в UNIX: обрабатывает ., .., абсолютные/относительные пути
    # возвращает список частей (без ведущего /)
    if target.startswith("/"):
        parts = target[1:].split("/")
    else:
        parts = (current + "/" + target).split("/")

    stack = []
    for part in parts:
        if part == "" or part == ".":
            continue
        elif part == "..":
            if stack:
                stack.pop()
        else:
            stack.append(part)
    return stack

def is_dir(vfs, path_parts):
    try:
        return isinstance(get_node(vfs, path_parts), dict)
    except:
        return False

def list_dir(vfs, path_parts):
    node = get_node(vfs, path_parts)
    if isinstance(node, dict):
        return list(node.keys())
    else:
        raise NotADirectoryError("Not a directory")