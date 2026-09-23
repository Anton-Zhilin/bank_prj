import pytest

from src.widget import mask_account_card

# 1. Тесты с использованием фикстур

def test_mask_account_card_with_fixture_card(valid_card_string: str) -> None:
    """Проверяет маскирование карты, используя фикстуру."""
    result = mask_account_card(valid_card_string)
    assert result == "Visa Platinum 7000 79** **** 6361"


def test_mask_account_card_with_fixture_account(valid_account_string: str) -> None:
    """Проверяет маскирование счета, используя фикстуру."""
    result = mask_account_card(valid_account_string)
    assert result == "Счет **4305"


# 2. Параметризация: Разные типы карт и счетов

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
    Проверяет что функция вызывает ValueError,
    если длина последнего слова не равна 16 или 20.
    """
    with pytest.raises(ValueError):
        mask_account_card(invalid_input)


