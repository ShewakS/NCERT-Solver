import json
from pathlib import Path


def save_json(path: str, data):
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with open(p, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def load_json(path: str):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)
