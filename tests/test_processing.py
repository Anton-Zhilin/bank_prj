import pytest

from src.processing import filter_by_state, sort_by_date

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
    """Проверяет, что функция корректно обрабатывает словари без ключа 'state'."""
    result = filter_by_state(data_without_state_key, "EXECUTED")
    assert result == []


def test_sort_by_date_descending(unsorted_data: list) -> None:
    """Проверяет сортировку по убыванию (значение reverse по умолчанию)."""
    assert sort_by_date(unsorted_data) == [
        {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
        {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
        {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
    ]


def test_sort_by_date_ascending(unsorted_data: list) -> None:
    """Проверяет сортировку по возрастанию (reverse=False)."""
    assert sort_by_date(unsorted_data, reverse=False) == [
        {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
        {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
        {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
        {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
    ]


def test_sort_by_date_same_dates(data_with_same_dates: list) -> None:
    """Проверяет корректность сортировки при одинаковых датах."""
    # При сортировке по убыванию
    result_desc = sort_by_date(data_with_same_dates, reverse=True)
    assert result_desc == data_with_same_dates

    # При сортировке по возрастанию
    result_asc = sort_by_date(data_with_same_dates, reverse=False)
    assert result_asc == data_with_same_dates


def test_sort_by_date_missing_dates(data_with_missing_dates: list) -> None:
    """Проверяет работу функции, если у словарей отсутствует ключ 'date'."""
    # При reverse=True элементы без даты уйдут в конец
    result_desc = sort_by_date(data_with_missing_dates, reverse=True)
    assert result_desc[0]["id"] == 1
    assert result_desc[1]["id"] == 3
    assert result_desc[2]["id"] == 2  # Элемент без даты в конце

    # При reverse=False элементы без даты окажутся в начале
    result_asc = sort_by_date(data_with_missing_dates, reverse=False)
    assert result_asc[0]["id"] == 2  # Элемент без даты в начале
    assert result_asc[1]["id"] == 3
    assert result_asc[2]["id"] == 1


# 2. Параметризация: различные статусы


@pytest.mark.parametrize(
    "state",
    [
        ("EXECUTED"),
        ("CANCELED"),
        ("PENDING"),
        ("FAILED"),
    ],
)
def test_filter_by_state_parametrized(sample_data: list, state: str) -> None:
    """Проверяет фильтрацию по разным статусам"""
    result = filter_by_state(sample_data, state)
    for item in result:
        assert item.get("state") == state


# 3. Параметризация: проверка аргумента reverse


@pytest.mark.parametrize(
    "reverse, expected_first_id", [(True, 41428829), (False, 939719570)]  # Самая поздняя дата  # Самая ранняя дата
)
def test_sort_by_date_reverse_param(unsorted_data: list, reverse: bool, expected_first_id: int) -> None:
    """Параметризованный тест: проверяет, что первый элемент соответствует направлению сортировки."""
    result = sort_by_date(unsorted_data, reverse=reverse)
    assert result[0]["id"] == expected_first_id


# 4. Параметризация: граничные случаи


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
        ([{"id": 1, "state": "X"}, {"id": 2, "state": "X"}], "X", [{"id": 1, "state": "X"}, {"id": 2, "state": "X"}]),
    ],
)
def test_filter_by_state_edge_cases(input_data: list, state: str, expected_result: list) -> None:
    """Параметризованный тест для проверки граничных случаев."""
    result = filter_by_state(input_data, state)
    assert result == expected_result


@pytest.mark.parametrize(
    "input_data",
    [
        ([]),  # Пустой список
        ([{"id": 1, "date": "2020-01-01"}]),  # Список из одного элемента
        (
            [{"id": 1, "date": "not_a_date"}, {"id": 2, "date": "2020-01-01"}]
        ),  # Некорректный формат даты (строка, не являющаяся ISO-датой)
    ],
)
def test_sort_by_date_edge_cases(input_data: list) -> None:
    """
    Параметризованный тест для проверки граничных случаев.
    Функция просто сортирует строки лексикографически.
    """
    result = sort_by_date(input_data)
    assert isinstance(result, list)
