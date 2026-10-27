import logging
import os

# НАСТРОЙКА ЛОГГЕРА ДЛЯ МОДУЛЯ masks


# Определяем путь к папке logs в корне проекта.
# __file__ = C:\...\bank_prj\src\masks.py
# os.path.dirname(__file__) = C:\...\bank_prj\src\
# os.path.dirname(os.path.dirname(__file__)) = C:\...\bank_prj\ (корень проекта)
LOG_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs")

# Путь к файлу логов
LOG_FILE = os.path.join(LOG_DIR, "masks.log")

# Создаём отдельный объект логгера для модуля masks
logger = logging.getLogger("masks")
logger.setLevel(logging.DEBUG)  # Уровень логирования не ниже DEBUG

# Создаём file_handler с перезаписью файла при каждом запуске (mode="w")
file_handler = logging.FileHandler(LOG_FILE, mode="w", encoding="utf-8")
file_handler.setLevel(logging.DEBUG)

# Создаём formatter: время | модуль | уровень | сообщение
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S")

# Устанавливаем formatter для handler
file_handler.setFormatter(file_formatter)

# Добавляем handler к логгеру
logger.addHandler(file_handler)


# ФУНКЦИИ МОДУЛЯ


def get_mask_card_number(card_number: str) -> str:
    """Маскирует номер банковской карты"""
    # Проверяем длину и содержимое номера карты
    if len(card_number) != 16 or not card_number.isdigit():
        # Логируем ошибку с уровнем ERROR
        logger.error(
            f"Неверный номер карты: '{card_number}'. " f"Ожидается 16 цифр, получено {len(card_number)} символов."
        )
        raise ValueError("Номер карты должен содержать 16 цифр")

    # Создаем замаскированный номер: первые 6 цифр + 6 звездочек + последние 4 цифры
    masked = card_number[:6] + "******" + card_number[-4:]

    # Разбиваем на блоки по 4 символа
    result = " ".join([masked[i : i + 4] for i in range(0, 16, 4)])

    # Логируем успешное выполнение с уровнем INFO
    logger.info(f"Номер карты успешно замаскирован: {result}")

    return result


def get_mask_account(account_number: str) -> str:
    """Маскирует номер банковского счета"""
    # Проверяем длину и содержимое номера счета
    if len(account_number) != 20 or not account_number.isdigit():
        # Логируем ошибку с уровнем ERROR
        logger.error(
            f"Неверный номер счета: '{account_number}'. "
            f"Ожидается 20 цифр, получено {len(account_number)} символов."
        )
        raise ValueError("Номер счета должен содержать 20 цифр")

    # Возвращаем маску: две звездочки + последние 4 цифры
    result = "**" + account_number[-4:]

    # Логируем успешное выполнение с уровнем INFO
    logger.info(f"Номер счета успешно замаскирован: {result}")

    return result


# ПРОВЕРОЧНЫЙ БЛОК


if __name__ == "__main__":
    print("Тестирование логирования модуля masks...\n")

    # Успешный случай — карта
    print("1. Маскируем номер карты:")
    card = get_mask_card_number("7000792289606361")
    print(f"   Результат: {card}\n")

    # Успешный случай — счёт
    print("2. Маскируем номер счета:")
    account = get_mask_account("73654108430135874305")
    print(f"   Результат: {account}\n")

    # Ошибочный случай — неверный номер карты
    print("3. Пробуем замаскировать неверный номер карты:")
    try:
        get_mask_card_number("12345")
    except ValueError as e:
        print(f"   Ошибка: {e}\n")

    # Ошибочный случай — неверный номер счёта
    print("4. Пробуем замаскировать неверный номер счета:")
    try:
        get_mask_account("abc")
    except ValueError as e:
        print(f"   Ошибка: {e}\n")

    print(f"Логи записаны в файл: {LOG_FILE}")
