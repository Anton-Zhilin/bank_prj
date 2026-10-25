import json
from typing import Any, Dict, List


def load_operations(filepath: str) -> List[Dict[str, Any]]:
    """
    Загружает данные о финансовых транзакциях из JSON-файла.
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            data = json.load(file)

            # Проверяем, что загруженные данные являются списком
            if isinstance(data, list):
                return data

            # Если данные есть, но это не список (например, словарь или строка)
            return []

    except (FileNotFoundError, json.JSONDecodeError):
        # FileNotFoundError: файл не найден
        # JSONDecodeError: файл пустой или содержит невалидный JSON
        return []

