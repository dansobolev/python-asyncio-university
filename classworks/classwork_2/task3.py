"""Task: Реализовать функцию, которая будет возвращать содержимое
файла, не блокируя выполнение других задач и не превышая
ограничение на скорость чтения (передается параметром в
функцию)."""


import asyncio
import time


async def read_from_file(
        path: str,
        read_size: int = 16,
        speed_time: int = 0.000001
) -> str:
    content = []
    with open(path, 'r') as file:
        chunk = file.read(read_size)
        while chunk:
            print(f"Chunk {chunk}")
            time_f = time.time()
            time_s = time.time()
            while time_s - time_f <= speed_time:
                content.append(chunk)
                time_s = time.time()
                chunk = file.read(read_size)
                await asyncio.sleep(0)

    return ''.join(content)


async def main():
    size = 3
    file_1 = '1.txt'
    file_2 = '2.txt'
    result = await asyncio.gather(read_from_file(file_1, size), read_from_file(file_2, size))
    print(result)


if __name__ == '__main__':
    asyncio.run(main())
