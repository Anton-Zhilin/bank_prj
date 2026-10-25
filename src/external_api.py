import os
from typing import Any, Dict

import requests
from dotenv import load_dotenv

# Загружаем переменные из .env при старте модуля
load_dotenv()


def get_amount_in_rub(transaction: Dict[str, Any]) -> float:
    """
    Возвращает сумму транзакции в рублях (float).
    Если валюта USD или EUR, запрашивает конвертацию через Exchange Rates Data API.
    """
    # 1. Извлекаем данные
    op_amount = transaction.get("operationAmount", {})
    if not op_amount:
        raise ValueError("В транзакции отсутствует поле 'operationAmount'")

    # .strip() убирает пробелы в начале и конце строки (например, "100.0 " -> "100.0")
    amount_str = str(op_amount.get("amount", "0"))
    currency_info = op_amount.get("currency", {})
    currency_code = str(currency_info.get("code", ""))

    amount = float(amount_str)

    # 2. Если валюта уже в рублях, просто возвращаем сумму
    if currency_code == "RUB":
        return amount

    # 3. Если валюта USD или EUR, делаем запрос к API конвертации
    if currency_code in ("USD", "EUR"):
        api_key = os.getenv("EXCHANGE_RATES_API_KEY")
        if not api_key:
            raise ValueError("API ключ не найден в переменных окружения (EXCHANGE_RATES_API_KEY)")

        # Формируем URL строго по примеру с сайта apilayer
        url = f"https://api.apilayer.com/exchangerates_data/convert?to=RUB&from={currency_code}&amount={amount}"
        headers = {"apikey": api_key}

        # Добавляем timeout=60, чтобы тесты не зависали при проблемах с сетью
        response = requests.get(url, headers=headers, timeout=60)
        response.raise_for_status()  # Выбросит исключение, если статус не 200 OK

        data = response.json()

        # Эндпоинт /convert возвращает итоговую сумму в ключе "result"
        if data.get("success") and "result" in data:
            return float(data["result"])
        else:
            raise ValueError(f"API вернул некорректный ответ: {data}")

    raise ValueError(f"Неподдерживаемая валюта для конвертации: {currency_code}")
