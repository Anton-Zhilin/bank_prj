import pytest

from src.generators import filter_by_currency, transaction_descriptions


# ТЕСТЫ ФУНКЦИИ filter_by_currency


# 1. Тесты с использованием фикстур


def test_filter_by_currency_usd(sample_transactions: list) -> None:
    """Проверяет фильтрацию транзакций по валюте USD."""
    usd_gen = filter_by_currency(sample_transactions, "USD")

    # Генератор должен выдать ровно 2 транзакции
    result = list(usd_gen)
    assert len(result) == 2
    assert result[0]["id"] == 939719570
    assert result[1]["id"] == 142264268


def test_filter_by_currency_rub(sample_transactions: list) -> None:
    """Проверяет фильтрацию транзакций по валюте RUB."""
    rub_gen = filter_by_currency(sample_transactions, "RUB")
    result = list(rub_gen)

    assert len(result) == 1
    assert result[0]["id"] == 873106923


def test_filter_by_currency_no_matches(sample_transactions: list) -> None:
    """Проверяет, что при отсутствии совпадений генератор пуст."""
    cny_gen = filter_by_currency(sample_transactions, "CNY")
    assert list(cny_gen) == []


def test_filter_by_currency_empty_list(empty_transactions: list) -> None:
    """Проверяет работу с пустым списком транзакций."""
    gen = filter_by_currency(empty_transactions, "USD")
    assert list(gen) == []


# 2. Параметризация: проверка различных валют


@pytest.mark.parametrize(
    "currency, expected_ids",
    [
        ("USD", [939719570, 142264268]),
        ("RUB", [873106923]),
        ("EUR", [414288290]),
        ("CNY", []),  # Валюта, которой нет в данных
    ]
)
def test_filter_by_currency_parametrized(sample_transactions: list, currency: str, expected_ids: list) -> None:
    """Параметризованный тест: проверяет корректность ID отфильтрованных транзакций."""
    gen = filter_by_currency(sample_transactions, currency)
    result_ids = [tx["id"] for tx in gen]
    assert result_ids == expected_ids


# 3. Тест на ошибки


def test_filter_by_currency_malformed_data(malformed_transactions: list) -> None:
    """
    Проверяет, что функция не падает с KeyError,
    если в словаре отсутствуют вложенные ключи.
    """
    # Должна найти только транзакцию с id=4, остальные проигнорирует без ошибок
    gen = filter_by_currency(malformed_transactions, "USD")
    result = list(gen)

    assert len(result) == 1
    assert result[0]["id"] == 4


# ТЕСТЫ ФУНКЦИИ transaction_descriptions


# 1. Тест с использованием фикстур (базовый сценарий)


def test_transaction_descriptions_basic(sample_transactions: list) -> None:
    """Проверяет, что генератор возвращает описания в правильном порядке."""
    gen = transaction_descriptions(sample_transactions)

    # Преобразуем генератор в список для удобной проверки
    result = list(gen)

    assert result == [
        "Перевод организации",
        "Перевод со счета на счет",
        "Вклад",
        "Оплата услуг"
    ]


# 2. Параметризация: различные входные списки


@pytest.mark.parametrize(
    "input_data, expected_descriptions",
    [
        # Один элемент
        ([{"description": "Тестовая операция"}], ["Тестовая операция"]),
        # Пустой список
        ([], []),
        # Несколько элементов с одинаковыми описаниями
        (
                [{"description": "А"}, {"description": "А"}, {"description": "Б"}],
                ["А", "А", "Б"]
        ),
    ]
)
def test_transaction_descriptions_parametrized(input_data: list, expected_descriptions: list) -> None:
    """Параметризованный тест: проверяет работу с разными наборами данных."""
    gen = transaction_descriptions(input_data)
    assert list(gen) == expected_descriptions


# 3. Тест на ошибки


def test_transaction_descriptions_missing_key(transactions_missing_description: list) -> None:
    """
    Проверяет, что функция не падает с KeyError,
    если у транзакции отсутствует ключ 'description'.
    """
    gen = transaction_descriptions(transactions_missing_description)
    result = list(gen)

    assert result == ["Перевод организации", "", "Оплата услуг"]


# 4. Проверка работы через next()


def test_transaction_descriptions_next_calls(sample_transactions: list) -> None:
     """Проверяет последовательный вызов next() на генераторе."""
     gen = transaction_descriptions(sample_transactions)

     assert next(gen) == "Перевод организации"
     assert next(gen) == "Перевод со счета на счет"
     assert next(gen) == "Вклад"
     assert next(gen) == "Оплата услуг"

     # После исчерпания генератора должен вызываться StopIteration
     with pytest.raises(StopIteration):
         next(gen)
