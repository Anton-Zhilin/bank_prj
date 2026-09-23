import pytest

from src.widget import mask_account_card, get_date

# 1. Тесты с использованием фикстур

def test_mask_account_card_with_fixture_card(valid_card_string: str) -> None:
    """Проверяет маскирование карты, используя фикстуру."""
    result = mask_account_card(valid_card_string)
    assert result == "Visa Platinum 7000 79** **** 6361"


def test_mask_account_card_with_fixture_account(valid_account_string: str) -> None:
    """Проверяет маскирование счета, используя фикстуру."""
    result = mask_account_card(valid_account_string)
    assert result == "Счет **4305"


def test_get_date_with_fixture(valid_date_string: str) -> None:
    """Проверяет преобразование даты, используя фикстуры."""
    assert get_date(valid_date_string) == "11.03.2024"


# 2. Параметризация: Корректные входные данные

@pytest.mark.parametrize(
    "input_data, expected_result",
    [
        # Карты (длина 16)
        ("Visa 4276550012345678", "Visa 4276 55** **** 5678"),
        ("МИР 2200000000000000", "МИР 2200 00** **** 0000"),
        ("Сложное Название Карты 1111222233334444", "Сложное Название Карты 1111 22** **** 4444"),
        # Счета (длина 20)
        ("Счет 40817810099910004312", "Счет **4312"),
        ("Bank Account 40817810099910004312", "Bank Account **4312"),
    ]
)
def test_mask_account_card_parametrized(input_data: str, expected_result: str) -> None:
    """
    Универсальный тест: проверяет, что функция верно определяет тип (карта/счет)
    по длине последнего слова и применяет соответствующую маску.
    """
    assert mask_account_card(input_data) == expected_result


@pytest.mark.parametrize(
    "date_string, expected",
    [
        ("2024-03-11T02:26:18.671407", "11.03.2024"),  # С микросекундами
        ("2023-12-31T23:59:59", "31.12.2023"),         # Без микросекунд
        ("2000-01-01T00:00:00", "01.01.2000"),         # Начало века
        ("2024-02-29T12:00:00", "29.02.2024"),         # Високосный год
        ("2024-03-11", "11.03.2024")                   # Только дата без времени

    ]
)
def test_get_date_valid_formats(date_string: str, expected: str) -> None:
    """Проверяет корректное преобразование различных валидных форматов ISO."""
    assert get_date(date_string) == expected


# 3. Параметризация: Некорректные входные данные (Ошибки)

@pytest.mark.parametrize(
    "invalid_input",
    [
        "Карта 12345",             # Слишком короткий номер карты
        "Счет 1234567890",         # Слишком короткий номер счета
        "Visa 1234abcd5678efgh",   # Буквы вместо номера
        "Просто текст без номера", # Нет номера в конце
        ""                         # Пустая строка
    ]
)
def test_mask_account_card_invalid_data(invalid_input: str) -> None:
    """
    Проверяет, что функция вызывает ValueError,
    если длина последнего слова не равна 16 или 20.
    """
    with pytest.raises(ValueError):
        mask_account_card(invalid_input)


# 3. Параметризация: невалидные входные данные
# ──────────────────────────────────────────────
@pytest.mark.parametrize(
    "invalid_input",
    [
        "",                          # Пустая строка
        "11.03.2024",                # Неправильный разделитель и порядок
        "2024-13-01T00:00:00",       # Несуществующий месяц
        "2024-02-30T00:00:00",       # Несуществующий день
        "Нету даты",                 # Просто текст
        "2024/03/11 02:26:18",       # Неправильные разделители
    ]
)
def test_get_date_invalid_formats(invalid_input: str) -> None:
    """
    Проверяет, что некорректные строки вызывают ValueError.
    """
    with pytest.raises(ValueError):
        get_date(invalid_input)

