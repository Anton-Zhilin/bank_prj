from masks import get_mask_card_number, get_mask_account
from datetime import datetime  # Импортируем модуль для работы с датой и временем


def mask_account_card(info: str) -> str:
    """
    Принимает строку с типом и номером карты или счета.
    Возвращает строку с типом и замаскированным номером.
    """
    # Разделяем входную строку на слова
    parts = info.split()

    # Последний элемент — это всегда номер
    number = parts[-1]

    # Все элементы кроме последнего — это тип ("Карта"" или "Счет")
    card_or_account_type = " ".join(parts[:-1])

    # Определяем, карта это или счет, по длине номера, и применяем нужную маску
    if len(number) == 16:
        masked_number = get_mask_card_number(number)
    elif len(number) == 20:
        masked_number = get_mask_account(number)
    else:
        raise ValueError("Неверная длина номера. Для карты нужно 16 цифр, для счета — 20.")

    # Формируем и возвращаем итоговую строку
    return f"{card_or_account_type} {masked_number}"


def get_date(date_string: str) -> str:
    """
    Принимает строку с датой в формате "2024-03-11T02:26:18.671407"
    и возвращает строку с датой в формате "ДД.ММ.ГГГГ" (например, "11.03.2024").
    """
    # Преобразуем строку в объект datetime (метод fromisoformat отлично парсит такой формат)
    date_obj = datetime.fromisoformat(date_string)

    # Форматируем объект datetime в строку нужного нам вида
    # %d - день, %m - месяц, %Y - год (4 цифры)
    return date_obj.strftime("%d.%m.%Y")


# Блок для проверки работы функций
if __name__ == "__main__":
    print("--- Проверка mask_account_card ---")
    test_data_cards = [
        "Maestro 1596837868705199",
        "Счет 64686473678894779589",
        "MasterCard 7158300734726758",
        "Счет 35383033474447895560",
        "Visa Classic 6831982476737658",
        "Visa Platinum 8990922113665229",
        "Visa Gold 5999414228426353",
        "Счет 73654108430135874305",
    ]

    for data in test_data_cards:
        print(f"{data} -> {mask_account_card(data)}")

    print("\n--- Проверка get_date ---")
    test_date = "2024-03-11T02:26:18.671407"
    print(f"Входная строка: {test_date}")
    print(f"Результат:      {get_date(test_date)}")
