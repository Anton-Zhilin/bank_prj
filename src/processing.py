from typing import List, Dict, Any


def filter_by_state(data: List[Dict[str, Any]], state: str = 'EXECUTED') -> List[Dict[str, Any]]:
    """
    Фильтрует список словарей по значению ключа 'state'.
    """
    return [item for item in data if item.get('state') == state]


def sort_by_date(data: List[Dict[str, Any]], reverse: bool = True) -> List[Dict[str, Any]]:
    """
    Сортирует список словарей по дате (date).
    """
    # Сортируем по ключу 'date'. Если ключа нет, подставляем пустую строку, чтобы избежать ошибки.
    return sorted(data, key=lambda x: x.get('date', ''), reverse=reverse)


# ==========================================
# Блок проверки и примеров использования
# ==========================================
if __name__ == "__main__":

    # Входные данные
    transactions = [
        {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
        {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
        {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
        {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'}
    ]


    # Вспомогательная функция для красивого вывода
    def print_list_pretty(data_to_print: List[Dict[str, Any]]) -> None:
        print("[")
        for item in data_to_print:
            print(f"  {item},")
        print("]")


    # Проверка 1: Фильтрация по умолчанию ('EXECUTED')
    print("Выход функции filter_by_state (по умолчанию 'EXECUTED'):")
    print_list_pretty(filter_by_state(transactions))


    # Проверка 2: Фильтрация если вторым значением передано 'CANCELED'
    print("Выход функции filter_by_state если вторым аргументом передано 'CANCELED':")
    print_list_pretty(filter_by_state(transactions, 'CANCELED'))


    # Проверка 3: Сортировка по дате (по убыванию - сначала самые новые)
    print("Выход функции sort_by_date (сортировка по убыванию):")
    print_list_pretty(sort_by_date(transactions))


    # Проверка 4: Сортировка по дате (по возрастанию - сначала самые старые)
    print("Выход функции sort_by_date (сортировка по возрастанию):")
    print_list_pretty(sort_by_date(transactions, reverse=False))