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


# Фикстуры для filter_by_state


@pytest.fixture
def sample_data() -> list:
    """Фикстура: список словарей с разными статусами."""
    return [
        {"id": 1, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 2, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
        {"id": 3, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
        {"id": 4, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
        {"id": 5, "state": "PENDING", "date": "2020-01-15T10:30:00.000000"},
    ]


@pytest.fixture
def empty_list() -> list:
    """Фикстура: пустой список."""
    return []


@pytest.fixture
def data_without_state_key() -> list:
    """Фикстура: словари без ключа 'state'."""
    return [
        {"id": 1, "date": "2020-01-01"},
        {"id": 2, "amount": 1000},
        {"id": 3},
    ]


@pytest.fixture
def data_with_no_matches() -> list:
    """Фикстура: данные, где нет статуса EXECUTED."""
    return [
        {"id": 1, "state": "CANCELED"},
        {"id": 2, "state": "PENDING"},
        {"id": 3, "state": "FAILED"},
    ]


# Фикстуры для sort_by_date


@pytest.fixture
def unsorted_data() -> list:
    """Фикстура: исходный неотсортированный список словарей."""
    return [
        {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
        {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
        {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
    ]


@pytest.fixture
def data_with_same_dates() -> list:
    """Фикстура: данные с одинаковыми датами."""
    return [
        {"id": 1, "date": "2020-01-01T00:00:00"},
        {"id": 2, "date": "2020-01-01T00:00:00"},
        {"id": 3, "date": "2020-01-01T00:00:00"},
    ]


@pytest.fixture
def data_with_missing_dates() -> list:
    """Фикстура: данные, где у некоторых словарей отсутствует ключ 'date'."""
    return [
        {"id": 1, "date": "2020-01-01T00:00:00"},
        {"id": 2},  # нет ключа date
        {"id": 3, "date": "2019-01-01T00:00:00"},
    ]
