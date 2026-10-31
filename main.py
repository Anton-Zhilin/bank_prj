import os
from typing import Any, Dict, List

from src.utils import load_operations
from src.file_readers import load_operations_csv, load_operations_excel
from src.processing import filter_by_state, sort_by_date, process_bank_search
from src.generators import filter_by_currency
from src.widget import mask_account_card, get_date


# ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ


def get_user_choice(prompt: str, valid_options: List[str]) -> str:
    """
    Запрашивает у пользователя ввод, пока он не введёт одно из допустимых значений.
    Сравнение регистронезависимое.
    """
    while True:
        user_input = input(prompt).strip()

        for option in valid_options:
            if user_input.lower() == option.lower():
                return option

        print(f'Неверный ввод. Доступные варианты: {", ".join(valid_options)}')


def format_transaction(transaction: Dict[str, Any]) -> str:
    """Форматирует одну транзакцию для вывода в консоль."""
    date_str = get_date(transaction.get("date", ""))
    description = transaction.get("description", "")

    from_info = transaction.get("from", "")
    to_info = transaction.get("to", "")

    # Явно проверяем, что значения являются строками, прежде чем передавать их в mask_account_card
    # Это защитит от float (NaN), которые pandas подставляет вместо пустых ячеек в Excel
    from_masked = mask_account_card(from_info) if isinstance(from_info, str) and from_info.strip() else ""
    to_masked = mask_account_card(to_info) if isinstance(to_info, str) and to_info.strip() else ""

    op_amount = transaction.get("operationAmount", {})

    # Также добавляем защиту для суммы и валюты на случай, если они пришли как float/NaN из Excel
    amount_raw = op_amount.get("amount", "0")
    amount = str(amount_raw).strip() if isinstance(amount_raw, (str, int, float)) else "0"

    currency_raw = op_amount.get("currency", {})
    currency_code = currency_raw.get("code", "")
    currency_code = str(currency_code).strip() if isinstance(currency_code, str) else ""

    lines = [f"{date_str} {description}"]

    if from_masked and to_masked:
        lines.append(f"{from_masked} -> {to_masked}")
    elif to_masked:
        lines.append(to_masked)

    lines.append(f"Сумма: {amount} {currency_code}")

    return "\n".join(lines)


# ОСНОВНАЯ ФУНКЦИЯ


def main() -> None:
    """Основная логика программы."""

    print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.")
    print("Выберите необходимый пункт меню:")
    print("1. Получить информацию о транзакциях из JSON-файла")
    print("2. Получить информацию о транзакциях из CSV-файла")
    print("3. Получить информацию о транзакциях из XLSX-файла")

    source_choice = get_user_choice("Ваш выбор: ", ["1", "2", "3"])

    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(base_dir, "data")

    # Загружаем данные в зависимости от выбора
    if source_choice == "1":
        filepath = os.path.join(data_dir, "operations.json")
        print("Для обработки выбран JSON-файл.")
        data = load_operations(filepath)
    elif source_choice == "2":
        filepath = os.path.join(data_dir, "transactions.csv")
        print("Для обработки выбран CSV-файл.")
        data = load_operations_csv(filepath)
    else:
        filepath = os.path.join(data_dir, "transactions_excel.xlsx")
        print("Для обработки выбран XLSX-файл.")
        data = load_operations_excel(filepath)

    if not data:
        print("Не удалось загрузить данные. Файл пуст или имеет неверный формат.")
        return

    # Фильтрация по статусу
    print('Введите статус, по которому необходимо выполнить фильтрацию.')
    print('Доступные для фильтровки статусы: EXECUTED, CANCELED, PENDING')

    status = get_user_choice("Статус: ", ["EXECUTED", "CANCELED", "PENDING"])
    data = filter_by_state(data, status)
    print(f'Операции отфильтрованы по статусу "{status}"')

    if not data:
        print("Не найдено ни одной транзакции, подходящей под ваши условия фильтрации.")
        return

    # Сортировка по дате
    sort_choice = get_user_choice("Отсортировать операции по дате? Да/Нет: ", ["Да", "Нет"])

    if sort_choice.lower() == "да":
        order_choice = get_user_choice(
            "Отсортировать по возрастанию или по убыванию? ",
            ["по возрастанию", "по убыванию"]
        )
        reverse = order_choice.lower() == "по убыванию"
        data = sort_by_date(data, reverse=reverse)

    # Фильтрация по валюте
    rub_only = get_user_choice("Выводить только рублевые транзакции? Да/Нет: ", ["Да", "Нет"])

    if rub_only.lower() == "да":
        data = list(filter_by_currency(data, "RUB"))

    # Фильтрация по слову в описании
    search_choice = get_user_choice(
        "Отфильтровать список транзакций по определенному слову в описании? Да/Нет: ",
        ["Да", "Нет"]
    )

    if search_choice.lower() == "да":
        search_word = input("Введите слово для поиска в описании: ").strip()
        if search_word:
            data = process_bank_search(data, search_word)

    # Вывод результатов
    print("\nРаспечатываю итоговый список транзакций...\n")

    if not data:
        print("Не найдено ни одной транзакции, подходящей под ваши условия фильтрации.")
        return

    print(f"Всего банковских операций в выборке: {len(data)}\n")

    for i, transaction in enumerate(data, start=1):
        print(format_transaction(transaction))
        if i < len(data):
            print()


# ТОЧКА ВХОДА


if __name__ == "__main__":
    main()