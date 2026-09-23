import pytest

from src.processing import filter_by_state


# 1. Тесты с использованием фикстур

def test_filter_by_state_default(sample_data: list) -> None:
    """Проверяет фильтрацию по статусу EXECUTED (значение по умолчанию)."""
    result = filter_by_state(sample_data)
    assert result == [
        {"id": 1, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 2, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
    ]


def test_filter_by_state_canceled(sample_data: list) -> None:
    """Проверяет фильтрацию по статусу CANCELED."""
    result = filter_by_state(sample_data, "CANCELED")
    assert result == [
        {"id": 3, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
        {"id": 4, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
    ]


def test_filter_by_state_empty_list(empty_list: list) -> None:
    """Проверяет, что функция корректно работает с пустым списком."""
    result = filter_by_state(empty_list)
    assert result == []


def test_filter_by_state_no_matches(data_with_no_matches: list) -> None:
    """Проверяет, что функция возвращает пустой список, если нет совпадений."""
    result = filter_by_state(data_with_no_matches, "EXECUTED")
    assert result == []


def test_filter_by_state_missing_key(data_without_state_key: list) -> None:
    """
    Проверяет, что функция корректно обрабатывает словари без ключа 'state'.
    """
    result = filter_by_state(data_without_state_key, "EXECUTED")
    assert result == []


# 2. Параметризация: различные статусы

@pytest.mark.parametrize("state",
    [
    ("EXECUTED"),
    ("CANCELED"),
    ("PENDING"),
    ("FAILED"),
    ]
)
def test_filter_by_state_parametrized(sample_data: list, state: str) -> None:
    """Проверяет фильтрацию по разным статусам """
    result = filter_by_state(sample_data, state)
    for item in result:
        assert item.get("state") == state


# 3. Параметризация: граничные случаи

@pytest.mark.parametrize(
    "input_data, state, expected_result",
    [
        # Пустой список с любым статусом
        ([], "EXECUTED", []),
        ([], "CANCELED", []),
        ([], "", []),
        # Список с одним элементом
        ([{"id": 1, "state": "EXECUTED"}], "EXECUTED", [{"id": 1, "state": "EXECUTED"}]),
        ([{"id": 1, "state": "EXECUTED"}], "CANCELED", []),
        # Все элементы с одинаковым статусом
        (
        [{"id": 1, "state": "X"}, {"id": 2, "state": "X"}],
        "X",
        [{"id": 1, "state": "X"}, {"id": 2, "state": "X"}]
        )
    ]
)
def test_filter_by_state_edge_cases(input_data: list, state: str, expected_result: list) -> None:
    """Параметризованный тест для проверки граничных случаев."""
    result = filter_by_state(input_data, state)
    assert result == expected_result

