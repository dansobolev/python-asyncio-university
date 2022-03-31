"""Task: https://docs.yandex.ru/docs/view?url=ya-disk-public%3A%2F%2FqqLXsWCMUapberSRCPON25kEPBsN79M9iEc6hvLLmawdB01x3jyzuqpNVoKIvcIIq%2FJ6bpmRyOJonT3VoXnDag%3D%3D&name=Task_classes.pdf"""


import random
from typing import List, Union


NAMES = ('John', 'James', 'Luther', 'Willard', 'Jake', 'Eugene',
         'Hugh', 'Glenn', 'Raymond', 'Caleb', 'Elliot')

WarriorType = Union['BaseWarrior', 'WarriorWithShield', 'WarriorExpert']


class BaseWarrior:
    def __init__(self, hp: int = None):
        self.strength = random.randint(20, 30)
        self.hp = hp or random.randint(100, 150)
        self.hp_base = self.hp
        self.name = random.choice(NAMES)
        self.died = False

    def receive_damage(self, strength: int):
        self.hp -= strength
        if self.hp < 0:
            self.died = True
            print(f"{self.name} получил {strength} урона и погиб")
        else:
            print(f"{self.name} получил {strength} урона. Осталось {self.hp} здоровья")

    def attack(self, enemy: WarriorType):
        enemy.receive_damage(self.strength)


class WarriorWithShield(BaseWarrior):
    def __init__(self):
        super().__init__()
        self.strength = random.randint(15, 25)
        self.shield = random.randint(5, 10)

    def receive_damage(self, strength: int):
        strength -= self.shield
        super().receive_damage(strength)

    def attack(self, enemy: WarriorType):
        enemy.receive_damage(self.strength)


class WarriorExpert(BaseWarrior):
    def __init__(self):
        super().__init__(hp=random.randint(100, 200))

    def receive_damage(self, strength: int):
        if self.hp / self.hp_base < 0.5:
            strength *= 1.2
        super().receive_damage(strength)

    def attack(self, enemy: WarriorType):
        if self.hp / self.hp_base < 0.5:
            enemy.receive_damage(self.strength * 2)
        else:
            enemy.receive_damage(self.strength)


class Army:
    def __init__(self, warriors: List[Union[BaseWarrior, WarriorWithShield, WarriorExpert]]):
        self.army = warriors

    @staticmethod
    def make_battle(army_first: 'Army', army_sec: 'Army'):
        count = 0
        army_first = army_first.army
        army_sec = army_sec.army
        while army_first and army_sec:
            warrior1 = army_first[0]
            warrior2 = army_sec[0]
            if count % 2 == 0:
                warrior1.attack(warrior2)
                warrior2.attack(warrior1)
            else:
                warrior2.attack(warrior1)
                warrior1.attack(warrior2)

            if warrior1.died:
                army_first.remove(warrior1)
            elif warrior2.died:
                army_sec.remove(warrior2)
            count += 1

        if not army_sec:
            print("Warriors from first army won the battle")
        else:
            print("Warriors from second army won the battle")


if __name__ == '__main__':
    warrior_types = [BaseWarrior, WarriorWithShield, WarriorExpert]
    army1 = Army([random.choice(warrior_types)() for _ in range(10)])
    army2 = Army([random.choice(warrior_types)() for _ in range(10)])

    Army.make_battle(army1, army2)
