from math import pi, tan


def Shape(name, area, perimeter):

    class __inner:

        def __init__(self, length):
            self.__name = name
            self.__length = length

        def setlength(self, length):
            assert length >= 0
            self.__length = length

        def calculate_perimeter(self):
            return perimeter(self.__length)

        def calculate_area(self):
            return area(self.__length)

        def __str__(self):
            area = self.calculate_area()
            perimeter = self.calculate_perimeter()
            return f"I'm a {self.__name} with area={area:.2f} and perimeter={perimeter:.2f}"

    return __inner


def RegularPolygon(name, n):
    return Shape(
        name=name,
        area=lambda s: (n * s * s) / (4 * tan(pi / n)),
        perimeter=lambda s: s * n,
    )


Circle = Shape(name="circle", area=lambda r: r**2 * pi, perimeter=lambda r: 2 * r * pi)
Triangle = RegularPolygon("triangle", 3)
Square = RegularPolygon("square", 4)
Pentagon = RegularPolygon("pentagon", 5)
Hexagon = RegularPolygon("hexagon", 6)

if __name__ == "__main__":
    shapes = [Triangle(3), Square(4), Triangle(5), Pentagon(12), Circle(3), Hexagon(1)]

    for shape in sorted(shapes, key=lambda s: s.calculate_area()):
        print(shape)
