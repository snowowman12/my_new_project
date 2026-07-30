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
