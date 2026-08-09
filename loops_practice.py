# ЗАДАНИЕ Имитация мониторинга нагрузки


import random
import time

ITERATIONS_COUNT = 10
LOAD_MIN = 0
LOAD_MAX = 100
LOAD_WARNING_THRESHOLD = 85
SLEEP_INTERVAL_SECONDS = 0.2


def monitor_load() -> None:
    """
    Имитирует мониторинг нагрузки системы в течение нескольких итераций.

    На каждой итерации генерируется случайное значение нагрузки в процентах.
    Если нагрузка превышает пороговое значение — выводится предупреждение.
    """
    for iteration in range(1, ITERATIONS_COUNT + 1):
        load = random.randint(LOAD_MIN, LOAD_MAX)
        print(f"[{iteration}/{ITERATIONS_COUNT}] Нагрузка: {load}%")

        if load > LOAD_WARNING_THRESHOLD:
            print(f"⚠️  Предупреждение: нагрузка превышает {LOAD_WARNING_THRESHOLD}%!")

        time.sleep(SLEEP_INTERVAL_SECONDS)


if __name__ == "__main__":
    monitor_load()


# ЗАДАНИЕ get_day_name


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


# ЗАДАНИЕ find_max

COUNT = 9
START = 1
STOP = START + COUNT  # верхняя граница для range (не включается)


def find_max(numbers: list[int]) -> int:
    """
    Находит максимальное значение в списке чисел вручную, без max().

    :param numbers: Непустой список чисел
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


# ЗАДАНИЕ list

numbers = list(range(1, 8))

for number in numbers:
    if number == 5:
        print("Встретили 5, прерываем цикл")
        break
    print(number)


# ЗАДАНИЕ list_comp

words = [f"str{i}" for i in range(10)]
print(words)


# ЗАДАНИЕ car_class


class Car:
    def __init__(self, brand: str, model: str, year: int):
        self.brand = brand
        self.model = model
        self.year = year

    def print_car_info(self) -> None:
        print(f"{self.brand} {self.model} ({self.year})")


car1 = Car("Hyundai", "Solaris", 2024)
car2 = Car("Audi", "A6", 2020)
car3 = Car("Niva", "Chevrolet", 2025)

car1.print_car_info()
car2.print_car_info()
car3.print_car_info()


# ЗАДАНИЕ Lead_class


class Lead:
    def __init__(self, name: str):
        self.name = name


def change_name(lead: Lead, new_name: str) -> None:
    lead.name = new_name


lead = Lead("Иван")
print(lead.name)

change_name(lead, "Илья")
print(lead.name)


# ЗАДАНИЕ class_Student


class Student:
    def __init__(self, name: str, age: int, grades: list[float]):
        self.name = name
        self.age = age
        self.grades = grades

    def get_avg_grade(self) -> float:
        if not self.grades:
            return 0.0
        return sum(self.grades) / len(self.grades)


students = [
    Student("Александр", 20, [4.5, 4.0, 4.8]),
    Student("Владимир", 21, [3.2, 4.0, 3.8]),
    Student("Михаил", 19, [4.9, 5.0, 4.1]),
]

good_students = [s for s in students if s.get_avg_grade() > 4.1]

for student in good_students:
    print(f"{student.name}: {student.get_avg_grade():.2f}")
