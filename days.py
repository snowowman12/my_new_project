def get_day_name(day: int) -> str:
    match day:
        case 1:
            return "Понедельник"
        case 2:
            return "Вторник"
        case 3:
            return "Среда"
        case 4:
            return "Четверг"
        case 5:
            return "Пятница"
        case 6:
            return "Суббота"
        case 7:
            return "Воскресенье"
        case _:
            raise ValueError(
                f"Некорректный номер дня: {day}. Ожидается число от 1 до 7."
            )


if __name__ == "__main__":
    for i in range(1, 8):
        print(i, "->", get_day_name(i))

    # Проверка на ошибку
    try:
        get_day_name(10)
    except ValueError as e:
        print("Ошибка:", e)
