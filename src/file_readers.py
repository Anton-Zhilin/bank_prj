import csv
import logging
import os
import pandas as pd

from typing import Any, Dict, List


# НАСТРОЙКА ЛОГГЕРА ДЛЯ МОДУЛЯ file_readers


# Определяем путь к папке logs в корне проекта.
# __file__ = C:\...\bank_prj\src\file_readers.py
# os.path.dirname(__file__) = C:\...\bank_prj\src\
# os.path.dirname(os.path.dirname(__file__)) = C:\...\bank_prj\ (корень проекта)
LOG_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs")

# Путь к файлу логов
LOG_FILE = os.path.join(LOG_DIR, "file_readers.log")

# Создаём отдельный объект логгера для модуля file_readers
logger = logging.getLogger("file_readers")
logger.setLevel(logging.DEBUG)  # Уровень логирования не ниже DEBUG

# Создаём file_handler с перезаписью файла при каждом запуске (mode="w")
file_handler = logging.FileHandler(LOG_FILE, mode="w", encoding="utf-8")
file_handler.setLevel(logging.DEBUG)

# Создаём formatter: время | модуль | уровень | сообщение
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S")

# Устанавливаем formatter для handler
file_handler.setFormatter(file_formatter)

# Добавляем handler к логгеру
logger.addHandler(file_handler)


def load_operations_csv(filepath: str) -> List[Dict[str, Any]]:
    """Загружает финансовые операции из CSV-файла"""
    logger.info(f"Попытка загрузить операции из CSV: {filepath}")
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            data = list(reader)

        logger.info(f"Успешно загружено {len(data)} операций из CSV.")
        return data

    except FileNotFoundError:
        logger.error(f"CSV файл не найден: {filepath}")
        return []
    except Exception as e:
        logger.error(f"Ошибка при чтении CSV файла {filepath}: {e}")
        return []


def load_operations_excel(filepath: str) -> List[Dict[str, Any]]:
    """Загружает финансовые операции из Excel-файла (.xlsx)"""
    logger.info(f"Попытка загрузить операции из Excel: {filepath}")
    try:
        # Читаем Excel файл
        df = pd.read_excel(filepath)

        # Заменяем NaN (пустые ячейки) на None для корректной работы с JSON/словарями
        df = df.where(pd.notnull(df), None)

        # Конвертируем DataFrame в список словарей
        data = df.to_dict(orient='records')

        logger.info(f"Успешно загружено {len(data)} операций из Excel.")
        return data

    except FileNotFoundError:
        logger.error(f"Excel файл не найден: {filepath}")
        return []
    except Exception as e:
        logger.error(f"Ошибка при чтении Excel файла {filepath}: {e}")
        return []

