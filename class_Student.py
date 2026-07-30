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
