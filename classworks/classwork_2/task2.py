"""Task: Реализовать функцию, которая будет возвращать содержимое
файла, не блокируя выполнение других задач."""


import asyncio


async def read_from_file(path: str, read_size: int = 16):
    content = []
    with open(path, 'r') as file:
        while True:
            chunk = file.read(read_size)
            print(f"Chunk {chunk}")
            if chunk:
                content.append(chunk)
            else:
                break
            await asyncio.sleep(0)

    return ''.join(content)


async def main():
    size = 4
    file_1 = '1.txt'
    file_2 = '2.txt'
    result = await asyncio.gather(read_from_file(file_1, size), read_from_file(file_2, size))
    print(result)


if __name__ == '__main__':
    asyncio.run(main())
