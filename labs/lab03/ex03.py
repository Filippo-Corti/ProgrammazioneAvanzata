import operator as ops
import sys


def isnum(x):
    try:
        float(x)
        return True
    except:
        return False


class PolishCalculator:

    __OPS = {
        "+": (ops.add, 2),
        "-": (ops.sub, 2),
        "*": (ops.mul, 2),
        "/": (ops.truediv, 2),
        "//": (ops.floordiv, 2),
        "**": (ops.pow, 2),
        "or": (ops.or_, 2),
        "and": (ops.and_, 2),
        "not": (ops.not_, 1),
        "neg": (lambda x: -x, 1),
        "pos": (lambda x: x, 1),
    }

    def __init__(self):
        self.__stack = []

    def __eval(self):
        op = self.__stack.pop()
        match op:
            case op if op in self.__OPS.keys():
                operation, opcount = self.__OPS[op]
                operands = [self.__eval() for _ in range(opcount)]
                return operation(*operands[::-1])
            case op if isnum(op):
                return float(op)
            case "T" | "F":
                return op == "T"
            case _:
                raise Exception(f"Unknown symbol {op}")

    def eval(self, str):
        self.__stack = str.split()
        return self.__eval()

    def __toinfix(self):
        op = self.__stack.pop()
        match op:
            case op if op in self.__OPS.keys():
                _, opcount = self.__OPS[op]
                operands = [self.__toinfix() for _ in range(opcount)]
                if opcount == 2:
                    return f"({operands[1]} {op} {operands[0]})"
                elif opcount == 1:
                    return f"{op}{operands[0]}"
                else:
                    raise Exception(f"Don't know how to print {op}")
            case op if isnum(op):
                return op
            case "T" | "F":
                return "True" if op == "T" else "False"
            case _:
                raise Exception(f"Unknown symbol {op}")

    def toinfix(self, str):
        self.__stack = str.split()
        return self.__toinfix()


calc = PolishCalculator()
print(f"Result: {calc.toinfix(sys.argv[1])}")
print(f"Result: {calc.eval(sys.argv[1])}")
