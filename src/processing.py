import re
from collections import Counter
from typing import Any, Dict, List


def filter_by_state(data: List[Dict[str, Any]], state: str = "EXECUTED") -> List[Dict[str, Any]]:
    """Фильтрует список словарей по значению ключа 'state'."""
    return [item for item in data if item.get("state") == state]


def sort_by_date(data: List[Dict[str, Any]], reverse: bool = True) -> List[Dict[str, Any]]:
    """Сортирует список словарей по дате (date)."""
    # Сортируем по ключу 'date'. Если ключа нет, подставляем пустую строку, чтобы избежать ошибки.
    return sorted(data, key=lambda x: x.get("date", ""), reverse=reverse)


def process_bank_search(data: List[Dict[str, Any]], search: str) -> List[Dict[str, Any]]:
    """Ищет банковские операции по описанию с использованием регулярных выражений."""
    # Экранируем специальные символы регулярных выражений в строке поиска
    # Компилируем паттерн с флагом IGNORECASE для регистронезависимого поиска
    pattern = re.compile(re.escape(search), re.IGNORECASE)

    result = []
    for transaction in data:
        # Получаем описание, если ключ отсутствует — используем пустую строку
        description = transaction.get("description", "")

        # Проверяем, что description является строкой
        if isinstance(description, str):
            # Ищем совпадение в описании
            if pattern.search(description):
                result.append(transaction)

    return result


def process_bank_operations(data: List[Dict[str, Any]], categories: List[str]) -> Dict[str, int]:
    """Подсчитывает количество банковских операций в каждой категории."""
    # Создаем множество категорий для быстрого поиска (с удалением пробелов)
    categories_set = {cat.strip() for cat in categories}

    # Извлекаем описания всех транзакций, очищая от пробелов
    descriptions = []
    for transaction in data:
        description = transaction.get("description", "")

        # Проверяем, что description является строкой
        if isinstance(description, str):
            # Очищаем от пробелов
            cleaned_description = description.strip()

            # Добавляем только если категория есть в списке
            if cleaned_description in categories_set:
                descriptions.append(cleaned_description)

    # Используем Counter для подсчета количества каждой категории
    counter = Counter(descriptions)

    # Преобразуем Counter в обычный словарь
    return dict(counter)