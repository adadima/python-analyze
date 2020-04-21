import math


def sqrt(x):
    return math.sqrt(x)


def func1(arg):
    print(f"Currying :) {arg}")


def func2():
    return func1


def func3():
    return func2


def func4():
    func3()()(3) + func3()()(4)


def func5():
    func1(sqrt(sqrt(sqrt(5))))
