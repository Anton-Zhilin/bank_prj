from typing import List, Dict, Any


def filter_by_state(data: List[Dict[str, Any]], state: str = 'EXECUTED') -> List[Dict[str, Any]]:
    """
    Фильтрует список словарей по значению ключа 'state'.
    """
    return [item for item in data if item.get('state') == state]


if __name__ == "__main__":
    transactions = [
        {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
        {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
        {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
        {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'}
    ]

    # Проверка 1
    result_executed = filter_by_state(transactions)
    print("Выход функции со статусом по умолчанию 'EXECUTED':")

    # Красивый вывод с помощью обычного print и цикла
    print("[")
    for item in result_executed:
        print(f"  {item},")
    print("]")


    # Проверка 2
    result_canceled = filter_by_state(transactions, 'CANCELED')
    print("Выход функции, если вторым аргументом передано 'CANCELED':")

    print("[")
    for item in result_canceled:
        print(f"  {item},")
    print("]")