# Playing with __dict__

class C:
    class_attr = 'The answer is 42'

    def __init__(self):
        self.instance_attr = 'a value'

    def meth(self):
        print("Running method...")

    def __str__(self):
        return self.instance_attr

class Point:
    __slots__ = ("x", "y")

    def __init__(self, x, y):
        self.x = x
        self.y = y