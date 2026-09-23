import pytest

from src.masks import get_mask_card_number, get_mask_account

# 1. Тесты с использованием фикстур


def test_mask_card_with_fixture(valid_card_number: str) -> None:
    """Проверяет маскирование номера карты, переданного через фикстуру."""
    assert get_mask_card_number(valid_card_number) == "7000 79** **** 6361"


def test_mask_another_card_with_fixture(another_valid_card: str) -> None:
    """Проверяет маскирование второго номера карты из фикстуры."""
    assert get_mask_card_number(another_valid_card) == "1234 56** **** 3456"


def test_mask_account_with_fixture(valid_account_number: str) -> None:
    """Проверяет маскирование номера счёта, переданного через фикстуру."""
    assert get_mask_account(valid_account_number) == "**7890"


def test_short_account_raises_error(short_account_number: str) -> None:
    """Явная проверка через фикстуру, что номер счёта короче 20 цифр вызывает ошибку."""
    with pytest.raises(ValueError, match="Номер счета должен содержать 20 цифр"):
        get_mask_account(short_account_number)


# 2. Параметризация: валидные номера карт


@pytest.mark.parametrize(
    "card_number, expected",
    [
        ("7000792289606361", "7000 79** **** 6361"),
        ("1234567890123456", "1234 56** **** 3456"),
        ("0000000000000000", "0000 00** **** 0000"),
    ],
)
def test_valid_card_numbers(card_number: str, expected: str) -> None:
    """Проверяет корректность маскирования номера карты для различных валидных номеров."""
    assert get_mask_card_number(card_number) == expected


@pytest.mark.parametrize(
    "account_number, expected",
    [("12345678901234567890", "**7890"), ("00000000000000000000", "**0000"), ("99999999999999999999", "**9999")],
)
def test_valid_account_numbers(account_number: str, expected: str) -> None:
    """Проверяет корректность маскирования счёта для различных валидных номеров."""
    assert get_mask_account(account_number) == expected


# 3. Параметризация: невалидные входные данные


@pytest.mark.parametrize(
    "invalid_input",
    [
        "",  # Пустая строка
        "123456",  # Слишком короткий номер
        "12345678901234567",  # 17 цифр (больше 16)
        "1234abcd5678efgh",  # Буквы вместо цифр
        "1234 5678 9012 3456",  # Пробелы в номере
        "1234-5678-9012-3456",  # Дефисы в номере
        " 123456789012345",  # Пробел в начале
    ],
)
def test_invalid_card_numbers_raise_value_error(invalid_input: str) -> None:
    """Проверяет, что невалидные входные данные вызывают ValueError."""
    with pytest.raises(ValueError, match="Номер карты должен содержать 16 цифр"):
        get_mask_card_number(invalid_input)


@pytest.mark.parametrize(
    "invalid_input",
    [
        "",  # Пустая строка
        "12345",  # 5 цифр (короткий номер)
        "123456789012345678901",  # 21 цифра (больше 20)
        "1234567890123456789 ",  # Пробел в конце
        "abcdefghij1234567890",  # Не все цифры
    ],
)
def test_invalid_account_numbers_raise_value_error(invalid_input: str) -> None:
    """Проверяет, что невалидные входные данные (в т.ч. короче 20) вызывают ValueError."""
    with pytest.raises(ValueError, match="Номер счета должен содержать 20 цифр"):
        get_mask_account(invalid_input)


# 4. Проверка структуры результата


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


def test_result_structure(valid_account_number: str) -> None:
    """Проверяет, что результат имеет правильную длину и формат."""
    result = get_mask_account(valid_account_number)

    # Общая длина должна быть 6 (2 звездочки + 4 цифры)
    assert len(result) == 6, "Замаскированный номер должен содержать ровно 6 символов"

    # Проверка префикса и суффикса
    assert result.startswith("**"), "Маска должна начинаться с '**'"
    assert result.endswith(valid_account_number[-4:]), "Маска должна заканчиваться последними 4 цифрами счёта"
