class Person:
    count = 0

    def __init__(self, name):
        self.name = name
        Person.count += 1

    @classmethod
    def  display_count(cls):
        print(f"Total persons created: {cls.count}")
person1 = Person("Alice")
Person.display_count()  # Output: Total persons created: 2
person2 = Person("Bob")
Person.display_count()  # Output: Total persons created: 2
