"""Task: Создайте 2 класса разных животных, отнаследованных от
класса Animal.
Определите метод make_noise, который будет уменьшать
сытость животного и в зависимости от сытости выводить
разное сообщение, специфичное для данного животного."""


from task1 import Animal


class Monkey(Animal):
    def make_noise(self, noise=1):
        self.satiety -= noise
        self.check_satiety_status()
        class_name = self.__class__.__name__
        if self.satiety <= 10:
            print(f"{class_name} is so hungry, please feed me")
        elif self.satiety >= 50:
            print(f"{class_name} monkey is full")


class Dinosaur(Animal):
    def make_noise(self, noise=1):
        self.satiety -= noise
        self.check_satiety_status()
        class_name = self.__class__.__name__
        if self.satiety <= 1:
            print(f"{self.__class__.__name__} is a little bit hungry")
        if self.satiety >= 80:
            print(f"{class_name} thank you for food")


monkey = Monkey()
monkey.make_noise()

dinosaur = Dinosaur(satiety=100)
dinosaur.make_noise(10)

# exception case
# monkey = Monkey(10)
# monkey.make_noise(20)
