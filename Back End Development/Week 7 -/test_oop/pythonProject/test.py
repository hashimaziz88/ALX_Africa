class Student:
    announcement = ""

    def __init__(self, grade):
        self.grade = grade

    def change_grade(self):
        self.grade = self.grade - 10


evans = Student(100)
print(evans.grade)
evans.change_grade()
print(evans.grade)