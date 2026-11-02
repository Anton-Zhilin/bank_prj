import os
from unittest.mock import Mock, patch

import pytest
import requests

from src.external_api import get_amount_in_rub


def test_get_amount_in_rub_rub(rub_transaction: dict) -> None:
    """Проверяет, что рубли возвращаются без запроса к API."""
    result = get_amount_in_rub(rub_transaction)
    assert result == 1500.50
    assert isinstance(result, float)


@patch("src.external_api.os.getenv")
@patch("src.external_api.requests.get")
def test_get_amount_in_rub_usd(mock_get: Mock, mock_getenv: Mock, usd_transaction: dict) -> None:
    """Проверяет конвертацию USD с мокированным ответом API."""
    mock_getenv.return_value = "test_secret_api_key"

    mock_response = Mock()
    mock_response.json.return_value = {
        "success": True,
        "query": {"from": "USD", "to": "RUB", "amount": 100.0},
        "info": {"rate": 92.5},
        "result": 9250.0,  # Итоговая сумма после конвертации
    }
    mock_response.raise_for_status = Mock()
    mock_get.return_value = mock_response

    result = get_amount_in_rub(usd_transaction)

    assert result == 9250.0
    assert isinstance(result, float)

    # Проверяем, что запрос был сделан с правильным URL и заголовками
    expected_url = "https://api.apilayer.com/exchangerates_data/convert?to=RUB&from=USD&amount=100.0"
    mock_get.assert_called_once_with(expected_url, headers={"apikey": "test_secret_api_key"}, timeout=60)


@patch("src.external_api.os.getenv")
def test_get_amount_in_rub_missing_api_key(mock_getenv: Mock, usd_transaction: dict) -> None:
    """Проверяет, что функция выбрасывает ошибку, если API ключ не задан."""
    mock_getenv.return_value = None

    with pytest.raises(ValueError, match="API ключ не найден в переменных окружения"):
        get_amount_in_rub(usd_transaction)


def test_get_amount_in_rub_unsupported_currency() -> None:
    """Проверяет обработку неподдерживаемой валюты."""
    transaction = {"operationAmount": {"amount": "100", "currency": {"code": "GBP"}}}
    with pytest.raises(ValueError, match="Неподдерживаемая валюта для конвертации: GBP"):
        get_amount_in_rub(transaction)
