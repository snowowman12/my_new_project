COUNT = 9
START = 1
STOP = START + COUNT  # верхняя граница для range (не включается)


def find_max(numbers: list[int]) -> int:
    """
    Находит максимальное значение в списке чисел вручную, без max().

    :param numbers: непустой список чисел
    :return: максимальное значение
    :raises ValueError: если список пуст
    """
    if not numbers:
        raise ValueError("Список чисел не должен быть пустым")

    current_max = numbers[0]
    for number in numbers[1:]:
        if number > current_max:
            current_max = number

    return current_max


if __name__ == "__main__":
    numbers = list(range(START, STOP))
    print("Список чисел:", numbers)

    result = find_max(numbers)
    print("Максимум:", result)

    numbers = list(range(1, 8))
