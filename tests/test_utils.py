import json
import pytest
from unittest.mock import patch, mock_open

from src.utils import load_operations


# 1. Тест успешной загрузки валидного списка


def test_load_operations_success() -> None:
    """Проверяет успешную загрузку корректного JSON-списка."""
    mock_json_data = json.dumps([
        {"id": 1, "state": "EXECUTED", "description": "Тестовая операция"}
    ])

    with patch("builtins.open", mock_open(read_data=mock_json_data)):
        result = load_operations("fake_path.json")

        assert isinstance(result, list)
        assert len(result) == 1
        assert result[0]["id"] == 1
        assert result[0]["state"] == "EXECUTED"


# 2. Тест: файл не найден


def test_load_operations_file_not_found() -> None:
    """Проверяет, что функция возвращает пустой список, если файл не существует."""
    # side_effect заставляет mock выбросить исключение при вызове open()
    with patch("builtins.open", side_effect=FileNotFoundError):
        result = load_operations("non_existent_file.json")
        assert result == []


# 3. Тест: файл пустой или содержит невалидный JSON


@pytest.mark.parametrize(
    "mock_data, test_name",
    [
        ("", "empty_file"),
        ("   ", "whitespace_only"),
        ("{ невалидный json }", "invalid_json_syntax"),
    ]
)
def test_load_operations_invalid_or_empty_json(mock_data: str, test_name: str) -> None:
    """Проверяет обработку пустых файлов или файлов с синтаксическими ошибками JSON."""
    with patch("builtins.open", mock_open(read_data=mock_data)):
        result = load_operations("invalid.json")
        assert result == []


# 4. Тест: JSON валиден, но это не список


@pytest.mark.parametrize(
    "mock_data, expected_type",
    [
        ('{"id": 1, "state": "EXECUTED"}', "dict"),
        ('"просто строка"', "string"),
        ('12345', "number"),
        ('null', "null"),
    ]
)
def test_load_operations_not_a_list(mock_data: str, expected_type: str) -> None:
    """Проверяет, что функция возвращает пустой список, если корневой элемент JSON — не список."""
    with patch("builtins.open", mock_open(read_data=mock_data)):
        result = load_operations("not_a_list.json")
        assert result == []


