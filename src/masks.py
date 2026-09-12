def get_mask_card_number(card_number: str) -> str:
    """
    Маскирует номер банковской карты.
    """
    # Проверяем длину и содержимое номера карты
    if len(card_number) != 16 or not card_number.isdigit():
        raise ValueError("Номер карты должен содержать 16 цифр")

    # Создаем замаскированный номер: первые 6 + 6 звездочек + последние 4
    masked = card_number[:6] + "******" + card_number[-4:]

    # Разбиваем на блоки по 4 символа
    result = " ".join([masked[i : i + 4] for i in range(0, 16, 4)])

    return result


def get_mask_account(account_number: str) -> str:
    """
    Маскирует номер банковского счета.
    """
    # Проверяем длину и содержимое номера счета
    if len(account_number) != 20 or not account_number.isdigit():
        raise ValueError("Номер счета должен содержать 20 цифр")

    # Возвращаем маску: две звездочки + последние 4 цифры
    return "**" + account_number[-4:]
