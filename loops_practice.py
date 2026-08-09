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
