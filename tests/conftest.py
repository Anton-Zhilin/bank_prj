import pytest


@pytest.fixture
def valid_card_number() -> str:
    """Фикстура: валидный 16-значный номер карты."""
    return "7000792289606361"


@pytest.fixture
def another_valid_card() -> str:
    """Фикстура: ещё один валидный номер карты."""
    return "1234567890123456"



