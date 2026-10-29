import csv
import pytest
import pandas as pd
from unittest.mock import patch, mock_open

from src.file_readers import load_operations_csv, load_operations_excel


# ТЕСТЫ ДЛЯ CSV


def test_load_operations_csv_success() -> None:
    """Проверяет успешную загрузку данных из CSV."""
    # Создаём строку, которая имитирует содержимое CSV-файла
    mock_csv_data = "id,state,amount\n1,EXECUTED,100.50\n2,CANCELED,200.00"

    # patch подменяет встроенную функцию open на mock_open
    with patch("builtins.open", mock_open(read_data=mock_csv_data)):
        result = load_operations_csv("fake_path.csv")

        # Проверяем результат
        assert len(result) == 2
        assert result[0]["id"] == "1"
        assert result[0]["state"] == "EXECUTED"
        assert result[1]["amount"] == "200.00"


def test_load_operations_csv_file_not_found() -> None:
    """Проверяет возврат пустого списка, если CSV файл не найден."""
    # side_effect заставляет open() выбросить исключение
    with patch("builtins.open", side_effect=FileNotFoundError):
        result = load_operations_csv("non_existent.csv")
        assert result == []


def test_load_operations_csv_invalid_file(tmp_path) -> None:
    """Проверяет обработку файла с неправильным форматом."""
    # Создаём JSON-файл вместо CSV
    test_file = tmp_path / "fake.csv"
    test_file.write_text('{"id": 1, "state": "EXECUTED"}', encoding="utf-8")

    # Функция должна вернуть пустой список при ошибке чтения
    result = load_operations_csv(str(test_file))
    assert result == []


# ТЕСТЫ ДЛЯ EXCEL


def test_load_operations_excel_success(tmp_path) -> None:
    """
    Проверяет успешную загрузку данных из Excel.
    Создаём реальный временный Excel-файл и читаем его.
    """

    # Создаём временный Excel-файл с тестовыми данными
    test_file = tmp_path / "test_transactions.xlsx"

    # Создаём DataFrame и сохраняем в Excel
    test_data = {
        "id": [1, 2],
        "state": ["EXECUTED", "CANCELED"],
        "amount": [100.50, 200.00]
    }
    df = pd.DataFrame(test_data)
    df.to_excel(test_file, index=False)

    # Вызываем функцию с путём к реальному файлу
    result = load_operations_excel(str(test_file))

    # Проверяем результат
    assert len(result) == 2
    assert result[0]["id"] == 1
    assert result[0]["state"] == "EXECUTED"
    assert result[1]["amount"] == 200.00


def test_load_operations_excel_file_not_found() -> None:
    """Проверяет возврат пустого списка, если Excel файл не найден."""
    # Просто передаём несуществующий путь — функция сама обработает ошибку
    result = load_operations_excel("non_existent_file.xlsx")
    assert result == []


def test_load_operations_excel_invalid_file(tmp_path) -> None:
    """Проверяет обработку файла с неправильным форматом."""
    # Создаём текстовый файл вместо Excel
    test_file = tmp_path / "fake.xlsx"
    test_file.write_text("Это не Excel файл", encoding="utf-8")

    # Функция должна вернуть пустой список при ошибке чтения
    result = load_operations_excel(str(test_file))
    assert result == []


