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


from enum import IntEnum, unique


@unique
class DayOfWeek(IntEnum):
    """Перечисление для исключения магических чисел."""

    MONDAY = 1
    TUESDAY = 2
    WEDNESDAY = 3
    THURSDAY = 4
    FRIDAY = 5
    SATURDAY = 6
    SUNDAY = 7


# Текстовые константы для исключения магических строк
RU_MONDAY = "Понедельник"
RU_TUESDAY = "Вторник"
RU_WEDNESDAY = "Среда"
RU_THURSDAY = "Четверг"
RU_FRIDAY = "Пятница"
RU_SATURDAY = "Суббота"
RU_SUNDAY = "Воскресенье"

# Границы для сообщения об ошибке
MIN_DAY_VALUE = min(day.value for day in DayOfWeek)
MAX_DAY_VALUE = max(day.value for day in DayOfWeek)
ERROR_TEMPLATE = (
    f"Некорректный номер дня: {{day}}. "
    f"Ожидается число от {MIN_DAY_VALUE} до {MAX_DAY_VALUE}."
)


def get_day_name(day: int) -> str:
    """Возвращает название дня недели по его порядковому номеру."""
    try:
        # Приведение к Enum убирает магическое число из match-case
        day_enum = DayOfWeek(day)
    except ValueError as error:
        raise ValueError(ERROR_TEMPLATE.format(day=day)) from error

    match day_enum:
        case DayOfWeek.MONDAY:
            return RU_MONDAY
        case DayOfWeek.TUESDAY:
            return RU_TUESDAY
        case DayOfWeek.WEDNESDAY:
            return RU_WEDNESDAY
        case DayOfWeek.THURSDAY:
            return RU_THURSDAY
        case DayOfWeek.FRIDAY:
            return RU_FRIDAY
        case DayOfWeek.SATURDAY:
            return RU_SATURDAY
        case DayOfWeek.SUNDAY:
            return RU_SUNDAY


if __name__ == "__main__":
    # Тест работы функции
    for i in range(MIN_DAY_VALUE, MAX_DAY_VALUE + 1):
        print(i, "->", get_day_name(i))


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


from datetime import datetime


class Car:

    def __init__(self, brand: str, model: str, year: int):
        self.brand = brand
        self.model = model
        self.year = year

    def print_car_info(self) -> None:
        print(f"{self.brand} {self.model} ({self.year})")

    def age(self) -> int:
        """Возвращает возраст автомобиля в годах."""
        current_year = datetime.now().year
        return current_year - self.year


# Пример использования:
car1 = Car("Hyundai", "Solaris", 2024)
car2 = Car("Audi", "A6", 2020)
car3 = Car("Niva", "Chevrolet", 2025)

car1.print_car_info()
print(f"Возраст: {car1.age()} г.")  # Выведет: 2 (для 2026 года)

car2.print_car_info()
print(f"Возраст: {car2.age()} г.")  # Выведет: 6

car3.print_car_info()
print(f"Возраст: {car3.age()} г.")  # Выведет: 1



# ЗАДАНИЕ Lead_class


class Lead:

    def __init__(self, name: str):
        self.name = name


def change_name(lead: Lead, new_name: str) -> None:
    lead.name = new_name


# объект класса Lead является изменяемым (mutable)
# строка lead.name = new_name не создает новый объект.
# находит существующий объект по адресу и перезаписывает его внутреннее поле name


lead = Lead("Иван")
# В оперативной памяти создается объект класса Lead со свойством name = "Иван".
# Переменная lead (глобальная) получает «адрес» этого объекта.

print(lead.name)

change_name(lead, "Илья")
# При передаче lead в функцию change_name, Python копирует адрес объекта в локальную переменную lead (внутри функции).
# В этот момент обе переменные (и внешняя, и внутренняя) смотрят на одну и ту же область памяти.
print(lead.name)


# ЗАДАНИЕ class_Student


class Student:
    """Класс, представляющий студента и его успеваемость."""

    def __init__(self, name: str, age: int, grades: list[float]):
        self.name = name
        self.age = age
        self.grades = grades

    def get_avg_grade(self) -> float:
        """Возвращает средний балл студента.

        Защищает от деления на ноль, если список оценок пуст.
        """
        if not self.grades:
            return 0.0
        return sum(self.grades) / len(self.grades)


# Константа для фильтрации (исключаем магические числа)
PASSING_AVG_GRADE = 4.1

if __name__ == "__main__":
    # Создаем тестовую выборку студентов
    students = [
        Student(
            name="Алексей", age=20, grades=[4.5, 4.0, 5.0, 4.2]
        ),  # Ср: 4.425 (> 4.1)
        Student(name="Мария", age=19, grades=[3.5, 4.0, 3.8, 4.1]),
        # Ср: 3.85  (< 4.1)
        Student(name="Иван", age=21, grades=[5.0, 5.0, 4.8, 4.9]),
        # Ср: 4.925 (> 4.1)
        Student(name="Ольга", age=22, grades=[]),
        # Ср: 0.0   (пустой список)
    ]

    # Фильтрация с помощью list comprehension
    excellent_students = [
        student for student in students if student.get_avg_grade() > PASSING_AVG_GRADE
    ]

    # Вывод результатов
    print(f"Студенты со средним баллом выше {PASSING_AVG_GRADE}:")
    for student in excellent_students:
        print(f"- {student.name} (Средний балл: {student.get_avg_grade():.2f})")
