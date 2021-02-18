class Person:
    def __init__(self, n, h, w):
        print("Hello! I am 初始化")
        self.name = n
        self.height = h
        self.weight = w

    def bmi(self):
        return self.weight / ((self.height / 100) ** 2)

someOne = Person('張xx',170,70)
print(someOne.name)
print(someOne.height)
print(someOne.weight)
print('bmi:',someOne.bmi())

someTwo = Person('王xx',160,45)
print(someTwo.name)
print(someTwo.height)
print(someTwo.weight)
print('bmi:',someTwo.bmi())