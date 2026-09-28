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


