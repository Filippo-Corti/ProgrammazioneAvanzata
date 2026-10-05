class rectangle:
    def __init__(self, w, h):
        self.__w = w
        self.__h = h

    def area(self):
        return self.__w * self.__h
    
    def perimeter(self):
        return 2 * (self.__w + self.__h)

    def __str__(self):
        return f"I'm a Rectangle! My sides are {self.__w} and {self.__h}, my area is {self.area()}"

class square(rectangle):
    def __init__(self, w):
        self.__w = w
        self.__h = w

    def __str__(self):
        return f"I'm a Square! My side is {self.__w} and my area is {self.area()}"
