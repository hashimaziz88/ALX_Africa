# This is a sample Python script.

# Press Ctrl+F5 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
# MAGIC METHODS/ DUNDER METHODS
class Point:
    def __init__(self, value_one, value_two):
        self.x = value_one
        self.y = value_two

    def __str__(self):
        return f"Point: ( X = {self.x}, Y = {self.y} )"

    def __del__(self):
        print(f"Object {self} has been destroyed.")


point1 = Point(1, 2)


def main():
    print(point1)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
    del point1
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
