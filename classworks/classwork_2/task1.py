"""Task: Реализовать асинхронную функцию проверки, что переданное число
является простым. Выводить сообщение на каждой итерации проверки
числа.
Проверить 2 числа. В процессе работы контекст выполнения должен
переключаться между проверкой этих чисел."""


import asyncio


async def is_prime(num: int):
    flag = False
    for i in range(2, num):
        print(f"Iteration {i - 1} for number {num}")
        await asyncio.sleep(0)
        if num % i == 0:
            flag = True
            print(f'Number {num} is not a prime number. End loop')
            break

    if not flag:
        print(f'Number {num} is prime number')


async def main():
    await asyncio.gather(is_prime(10), is_prime(5))


if __name__ == '__main__':
    asyncio.run(main())
