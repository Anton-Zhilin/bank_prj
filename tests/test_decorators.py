import os
from pathlib import Path

import pytest

from src.decorators import log

# ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ ДЛЯ ТЕСТИРОВАНИЯ


@log()
def add_numbers(x: int, y: int) -> int:
    """Функция сложения для тестирования."""
    return x + y


@log()
def divide_numbers(x: int, y: int) -> float:
    """Функция деления для тестирования ошибок."""
    return x / y


@log()
def greet(name: str) -> str:
    """Функция приветствия."""
    return f"Hello, {name}!"


# 1. ТЕСТЫ УСПЕШНОГО ВЫПОЛНЕНИЯ (ВЫВОД В КОНСОЛЬ)


def test_log_success_console(capsys: pytest.CaptureFixture) -> None:
    """Проверяет логирование успешного выполнения в консоль."""
    result = add_numbers(1, 2)

    assert result == 3

    captured = capsys.readouterr()
    assert "add_numbers ok" in captured.out


def test_log_success_with_kwargs(capsys: pytest.CaptureFixture) -> None:
    """Проверяет логирование при использовании именованных аргументов."""
    result = greet(name="Alice")

    assert result == "Hello, Alice!"

    captured = capsys.readouterr()
    assert "greet ok" in captured.out


def test_log_success_no_arguments(capsys: pytest.CaptureFixture) -> None:
    """Проверяет логирование функции без аргументов."""

    @log()
    def no_args_func() -> str:
        return "test"

    result = no_args_func()

    assert result == "test"

    captured = capsys.readouterr()
    assert "no_args_func ok" in captured.out


# 2. ТЕСТЫ ОШИБОК (ВЫВОД В КОНСОЛЬ)


def test_log_error_console(capsys: pytest.CaptureFixture) -> None:
    """Проверяет логирование ошибки в консоль."""
    with pytest.raises(ZeroDivisionError):
        divide_numbers(1, 0)

    captured = capsys.readouterr()
    assert "divide_numbers error: ZeroDivisionError" in captured.out
    assert "Inputs: (1, 0), {}" in captured.out


def test_log_error_with_kwargs(capsys: pytest.CaptureFixture) -> None:
    """Проверяет логирование ошибки с именованными аргументами."""

    @log()
    def func_with_kwargs(a: int, b: int) -> int:
        raise ValueError("Тестовая ошибка")

    with pytest.raises(ValueError):
        func_with_kwargs(a=10, b=20)

    captured = capsys.readouterr()
    assert "func_with_kwargs error: ValueError" in captured.out
    assert "Inputs: (), {'a': 10, 'b': 20}" in captured.out


def test_log_error_preserves_exception(capsys: pytest.CaptureFixture) -> None:
    """Проверяет, что декоратор не поглощает исключение, а пробрасывает его дальше."""
    with pytest.raises(TypeError):

        @log()
        def raise_type_error() -> None:
            raise TypeError("Неправильный тип")

        raise_type_error()

    captured = capsys.readouterr()
    assert "raise_type_error error: TypeError" in captured.out


# 3. ТЕСТЫ ЗАПИСИ В ФАЙЛ


def test_log_success_to_file(tmp_path: Path) -> None:
    """Проверяет запись успешного выполнения в файл."""
    log_file = tmp_path / "test_success.log"

    @log(filename=str(log_file))
    def file_func(x: int) -> int:
        return x * 2

    result = file_func(5)

    assert result == 10
    assert log_file.exists()

    content = log_file.read_text(encoding="utf-8")
    assert "file_func ok" in content


def test_log_error_to_file(tmp_path: Path) -> None:
    """Проверяет запись ошибки в файл."""
    log_file = tmp_path / "test_error.log"

    @log(filename=str(log_file))
    def error_func(x: int) -> int:
        raise RuntimeError("Ошибка выполнения")

    with pytest.raises(RuntimeError):
        error_func(42)

    assert log_file.exists()

    content = log_file.read_text(encoding="utf-8")
    assert "error_func error: RuntimeError" in content
    assert "Inputs: (42,), {}" in content
