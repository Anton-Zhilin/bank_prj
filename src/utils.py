import json
import logging
import os
from typing import Any, Dict, List


# НАСТРОЙКА ЛОГГЕРА ДЛЯ МОДУЛЯ utils


# Определяем путь к папке logs в корне проекта.
# __file__ = C:\...\bank_prj\src\utils.py
# os.path.dirname(__file__) = C:\...\bank_prj\src\
# os.path.dirname(os.path.dirname(__file__)) = C:\...\bank_prj\ (корень проекта)
LOG_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs")

# Путь к файлу логов
LOG_FILE = os.path.join(LOG_DIR, "utils.log")

# Создаём отдельный объект логгера для модуля utils
logger = logging.getLogger("utils")
logger.setLevel(logging.DEBUG)  # Уровень логирования не ниже DEBUG

# Создаём file_handler с перезаписью файла при каждом запуске (mode="w")
file_handler = logging.FileHandler(LOG_FILE, mode="w", encoding="utf-8")
file_handler.setLevel(logging.DEBUG)

# Создаём formatter: время | модуль | уровень | сообщение
file_formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

# Устанавливаем formatter для handler
file_handler.setFormatter(file_formatter)

# Добавляем handler к логгеру
logger.addHandler(file_handler)


# ФУНКЦИИ МОДУЛЯ


def load_operations(filepath: str) -> List[Dict[str, Any]]:
    """
    Загружает данные о финансовых транзакциях из JSON-файла.

    Args:
        filepath: Путь к JSON-файлу.

    Returns:
        Список словарей с данными транзакций.
        Возвращает пустой список, если файл не найден, пуст или содержит не список.
    """
    logger.info(f"Попытка загрузить операции из файла: {filepath}")

    try:
        with open(filepath, "r", encoding="utf-8") as file:
            data = json.load(file)

            # Проверяем, что загруженные данные являются списком
            if isinstance(data, list):
                logger.info(
                    f"Файл успешно загружен. Получено операций: {len(data)}"
                )
                return data

            # Если данные есть, но это не список (например, словарь или строка)
            logger.error(
                f"Ожидался список операций, но получен тип: {type(data).__name__}"
            )
            return []

    except FileNotFoundError:
        # Файл не найден
        logger.error(f"Файл не найден: {filepath}")
        return []

    except json.JSONDecodeError as e:
        # Файл пустой или содержит невалидный JSON
        logger.error(f"Ошибка парсинга JSON в файле {filepath}: {e}")
        return []


# ПРОВЕРОЧНЫЙ БЛОК


if __name__ == "__main__":
    print("Тестирование логирования модуля utils...\n")

    # Определяем путь к файлу operations.json в папке data
    data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
    operations_file = os.path.join(data_dir, "operations.json")

    print(f"1. Загружаем файл: {operations_file}")
    operations = load_operations(operations_file)
    print(f"   Загружено операций: {len(operations)}\n")

    print("2. Пробуем загрузить несуществующий файл:")
    result = load_operations("non_existent_file.json")
    print(f"   Результат: {result}\n")

