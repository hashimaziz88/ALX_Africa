import math


class Shape:
    def area(self):
        """Raise NotImplementedError to indicate this method should be overridden."""
        raise NotImplementedError("Subclasses must override area() method")


class Rectangle(Shape):
    def __init__(self, length, width):
        """Initialize rectangle attributes."""
        self.length = length
        self.width = width

    def area(self):
        """Calculate and return the area of the rectangle."""
        return self.length * self.width


class Circle(Shape):
    def __init__(self, radius):
        """Initialize circle attributes."""
        self.radius = radius

    def area(self):
        """Calculate and return the area of the circle."""
        return math.pi * (self.radius ** 2)
