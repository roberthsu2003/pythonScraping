class Person:
    def __init__(self, n, h, w):
        print("Hello! I am 初始化")
        self.name = n
        self.height = h
        self.weight = w

    def bmi(self):
        return self.weight / ((self.height / 100) ** 2)

def sayHello(name):
    print('Hello',name)

