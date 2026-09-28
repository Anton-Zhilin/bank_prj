from typing import Any, Dict, Iterator, List


def filter_by_currency(transactions: List[Dict[str, Any]], currency: str) -> Iterator[Dict[str, Any]]:
    """Фильтрует список транзакций по заданной валюте."""
    for transaction in transactions:
        # Безопасно извлекаем код валюты, чтобы избежать KeyError,
        # если структура словаря окажется неполной
        transaction_currency = transaction.get("operationAmount", {}).get("currency", {}).get("code")

        if transaction_currency == currency:
            yield transaction


def transaction_descriptions(transactions: List[Dict[str, Any]]) -> Iterator[str]:
    """Принимает список словарей с транзакциями и возвращает описание каждой операции по очереди."""
    for transaction in transactions:
        yield transaction.get("description", "")


def card_number_generator(start: int, stop: int) -> Iterator[str]:
    """Генератор номеров банковских карт в формате XXXX XXXX XXXX XXXX."""
    # Проверка корректности диапазона
    if start < 1 or stop > 9999999999999999:
        raise ValueError("Диапазон номеров карт должен быть от 1 до 9999999999999999")

    for i in range(start, stop + 1):
        # Превращаем число в строку
        num_str = str(i)

        # Добавляем нужное количество нулей слева, чтобы получить ровно 16 цифр
        num_str = '0' * (16 - len(num_str)) + num_str

        # Разбиваем на блоки по 4 цифры
        formatted_card = f"{num_str[:4]} {num_str[4:8]} {num_str[8:12]} {num_str[12:]}"
        yield formatted_card