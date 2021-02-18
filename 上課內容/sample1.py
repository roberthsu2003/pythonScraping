import PERSON
someOne = PERSON.Person('張xx',170,70)
print(someOne.name)
print(someOne.height)
print(someOne.weight)
print('bmi:',someOne.bmi())

someTwo = PERSON.Person('王xx',160,45)
print(someTwo.name)
print(someTwo.height)
print(someTwo.weight)
print('bmi:',someTwo.bmi())