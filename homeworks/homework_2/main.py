"""Task: Необходимо написать программу, реализующую сеанс одновременной
игры в шахматы. Играет гроссмейстер и 8 любителей. Гроссмейстер
делает ход за 3-5 секунд, любители за 30-50 секунд. Первыми ходят
любители. Для простоты считаем, что партия продолжается 20 ходов.
На каждый ход любителя выводить сообщение, что он сделал ход и
его имя. На каждый ход гроссмейстера, аналогично и выводить имя
любителя, против которого он играет.
Выводить сообщение об окончании партии (с именем шахматиста) и об
окончании всех партий."""


import asyncio
import random


NAMES = ('John', 'James', 'Luther', 'Willard',
         'Hugh', 'Glenn', 'Raymond', 'Jake')
GRANDMASTER = 'Elliot'


class BasePlayer:
    def __init__(self, game_duration: int = 20):
        self.game_duration = game_duration
        self.move_num = 0

    async def move(self):
        pass

    def check_duration(self):
        print(f"Ход номер {self.move_num}")
        if self.move_num == self.game_duration:
            return True
        self.move_num += 1


class OrdinaryPlayer(BasePlayer):
    def __init__(self):
        super().__init__()
        self.name = random.choice(NAMES)

    async def move(self):
        while not self.check_duration():
            move_time = random.randint(4, 5)
            print(f"Любитель {self.name} сделал ход sleep for {move_time}")
            print(f"Любитель {self.name} will sleep for {move_time}")
            await asyncio.sleep(move_time)
        return


class GrandMasterPlayer(BasePlayer):
    def __init__(self):
        super().__init__()
        self.name = GRANDMASTER

    async def move(self):
        while not self.check_duration():
            move_time = random.randint(1, 2)
            print(f"Грандмастер {self.name} сделал ход. Играет против любителя some_name")
            print(f"Грандмастер {self.name} will sleep for {move_time}")
            await asyncio.sleep(move_time)
        return


async def main():
    players = [OrdinaryPlayer() for _ in range(8)] + [GrandMasterPlayer()]
    await asyncio.gather(*[asyncio.create_task(player.move()) for player in players])


asyncio.run(main())
