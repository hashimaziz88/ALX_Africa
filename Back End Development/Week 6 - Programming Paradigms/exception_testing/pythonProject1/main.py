# This is a sample Python script.

# Press Ctrl+F5 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import unittest

def add(x,y):
    """Returns the sum of two numbers."""
    return x + y

class TestAdd(unittest.TestCase):

    def test_add_positive(self):
        result = add(5, 3)
        self.assertEqual(result, 8)

    def test_add_negative(self):
        result = add(-2, 7)
        self.assertEqual(result, 5)




# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    unittest.main()
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
