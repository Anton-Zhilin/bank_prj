import os
import requests
from typing import Any, Dict
from dotenv import load_dotenv

# Загружаем переменные из .env при старте модуля
load_dotenv()


def get_amount_in_rub(transaction: Dict[str, Any]) -> float:
    """
    Возвращает сумму транзакции в рублях (float).
    Если валюта USD или EUR, запрашивает актуальный курс через Exchange Rates Data API.
    """
    # 1. Извлекаем данные
    op_amount = transaction.get("operationAmount", {})
    if not op_amount:
        raise ValueError("В транзакции отсутствует поле 'operationAmount'")

    amount_str = str(op_amount.get("amount", "0"))
    currency_info = op_amount.get("currency", {})
    currency_code = str(currency_info.get("code", ""))

    amount = float(amount_str)

    # 2. Если валюта уже в рублях, просто возвращаем сумму
    if currency_code == "RUB":
        return amount

    # 3. Если валюта USD или EUR, делаем запрос к API
    if currency_code in ("USD", "EUR"):
        api_key = os.getenv("EXCHANGE_RATES_API_KEY")
        if not api_key:
            raise ValueError("API ключ не найден в переменных окружения (EXCHANGE_RATES_API_KEY)")

        url = f"https://api.apilayer.com/exchangerates_data/latest?symbols=RUB&base={currency_code}"
        headers = {"apikey": api_key}

        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Выбросит исключение, если статус не 200 OK

        data = response.json()

        # Структура ответа apilayer: {"success": true, "rates": {"RUB": 92.5}}
        rate = data.get("rates", {}).get("RUB")

        if rate is None:
            raise ValueError(f"Не удалось получить курс RUB для валюты {currency_code}")

        return float(amount * rate)

    raise ValueError(f"Неподдерживаемая валюта для конвертации: {currency_code}")

