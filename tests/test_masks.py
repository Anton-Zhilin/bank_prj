import pytest

from src.masks import get_mask_card_number

# 1.1. Тест с использованием фикстур

def test_mask_card_with_fixture(valid_card_number: str) -> None:
    """Проверяет маскирование номера, переданного через фикстуру."""
    assert get_mask_card_number(valid_card_number) == "7000 79** **** 6361"


def test_mask_another_card_with_fixture(another_valid_card: str) -> None:
    """Проверяет маскирование второго номера из фикстуры."""
    assert get_mask_card_number(another_valid_card) == "1234 56** **** 3456"

# 2.1. Параметризация: валидные номера карт

@pytest.mark.parametrize(
    "card_number, expected",
    [
        ("7000792289606361", "7000 79** **** 6361"),
        ("1234567890123456", "1234 56** **** 3456"),
        ("0000000000000000", "0000 00** **** 0000"),   # Все нули
    ]
)
def test_valid_card_numbers(card_number: str, expected: str) -> None:
    """Проверяет корректность маскирования для различных валидных номеров."""
    assert get_mask_card_number(card_number) == expected

# 3.1. Параметризация: невалидные входные данные

@pytest.mark.parametrize(
    "invalid_input",
    [
        "",                  # Пустая строка
        "123456",            # Слишком короткий номер
        "12345678901234567", # 17 цифр — слишком длинный
        "1234abcd5678efgh",  # Буквы вместо цифр
        "1234 5678 9012 3456",  # Пробелы в номере
        "1234-5678-9012-3456",  # Дефисы в номере
        "123456789012345!",  # Спецсимвол в конце
        " 123456789012345",  # Пробел в начале
    ]
)
def test_invalid_card_numbers_raise_value_error(invalid_input: str) -> None:
    """Проверяет, что невалидные входные данные вызывают ValueError."""
    with pytest.raises(ValueError):
        get_mask_card_number(invalid_input)

# 4.1. Проверка структуры результата

def test_result_format_structure(valid_card_number: str) -> None:
    """Проверяет, что результат состоит из 4 блоков по 4 символа."""
    result = get_mask_card_number(valid_card_number)
    blocks = result.split(" ")

    assert len(blocks) == 4, "Результат должен содержать 4 блока"
    for block in blocks:
        assert len(block) == 4, f"Каждый блок должен содержать 4 символа, получено: {block}"


def test_masked_positions_are_asterisks(valid_card_number: str) -> None:
    """Проверяет, что звёздочки стоят именно на позициях 7–12."""
    result = get_mask_card_number(valid_card_number)
    # Убираем пробелы для проверки позиций
    compact = result.replace(" ", "")

    assert compact[6:12] == "******", "Позиции 7–12 должны быть замаскированы"
