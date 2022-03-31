"""Task: Напишите код, описывающий класс Animal, добавьте
атрибуты имени животного и его сытости, метод eat -
увеличивающий “сытость” животного, методы get_name и
set_name, конструктор класса Animal выводящий
сообщение при создании объекта.
Создайте несколько объектов и вызовите методы
set_name/get_name/eat."""


class NegativeSatietyValueException(Exception):
    pass


class Animal:
    def __init__(self, name='John', satiety=10):
        self.name = name
        self.satiety = satiety
        print(f"Create new Animal object, name: {self.name}, satiety: {self.satiety}")

    def eat(self):
        self.satiety += 1

    def get_name(self):
        return self.name

    def set_name(self, new_name):
        self.name = new_name

    def check_satiety_status(self):
        if self.satiety < 0:
            raise NegativeSatietyValueException(f"Satiety value can't be negative, now satiety={self.satiety}")


if __name__ == '__main__':
    lion = Animal(name='Lion', satiety=100)
    lion.eat()
    print("Lion satiety: ", lion.satiety)
    print("Lion name: ", lion.get_name())
    lion.set_name('Old lion')  # setting new name
    print("New Lion name: ", lion.get_name())
