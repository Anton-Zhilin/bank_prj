import pytest

# Фикстуры для get_mask_card_number

@pytest.fixture
def valid_card_number() -> str:
    """Фикстура: валидный 16-значный номер карты."""
    return "7000792289606361"

@pytest.fixture
def another_valid_card() -> str:
    """Фикстура: ещё один валидный номер карты."""
    return "1234567890123456"

# Фикстуры для get_mask_account

@pytest.fixture
def valid_account_number() -> str:
    """Фикстура: валидный 20-значный номер счета."""
    return "12345678901234567890"

@pytest.fixture
def short_account_number() -> str:
    """Фикстура: номер счета короче ожидаемой длины (19 цифр)."""
    return "1234567890123456789"

# Фикстуры для mask_account_card

@pytest.fixture
def valid_card_string() -> str:
    """Строка с типом карты и номером."""
    return "Visa Platinum 7000792289606361"

@pytest.fixture
def valid_account_string() -> str:
    """Строка со словом 'Счет' и номером счета."""
    return "Счет 73654108430135874305"

# Фикстуры для get_date

@pytest.fixture
def valid_date_string() -> str:
    """Фикстура: стандартная строка даты в формате ISO 8601 с микросекундами."""
    return "2024-03-11T02:26:18.671407"

