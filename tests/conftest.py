import pytest


@pytest.fixture
def valid_card_number() -> str:
    """Фикстура: валидный 16-значный номер карты."""
    return "7000792289606361"

@pytest.fixture
def another_valid_card() -> str:
    """Фикстура: ещё один валидный номер карты."""
    return "1234567890123456"

@pytest.fixture
def valid_account_number() -> str:
    """Фикстура: валидный 20-значный номер счета."""
    return "12345678901234567890"

@pytest.fixture
def short_account_number() -> str:
    """Фикстура: номер счета короче ожидаемой длины (19 цифр)."""
    return "1234567890123456789"

