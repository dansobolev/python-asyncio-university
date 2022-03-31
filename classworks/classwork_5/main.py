"""
Task 1:
Разработать таблицы и модели для информационной системы по
обслуживанию библиотеки.

В системе хранятся следующие сведения:
 - названия книг;
 - год издания;
 - количество страниц;
 - стоимость;
 - количество имеющихся в библиотеке экземпляров конкретной книги;
 - сведения о студентах, которым выданы конкретные книги;
 - названия факультетов, в учебном процессе которых
   используется указанная книга.

О студентах известно: ФИО, название факультета.

Task 2:
Написать следующие функции:
1 Добавление студента.
2 Добавление книги.
3 Выдача книги студенту: одному студенту не может быть выдано
более одного экземпляра книги.
4 Получение книги обратно от студента

Task 3:
Написать функции, возвращающую следующие данные:
1 Средний год издания книг и суммарное количество страниц,
прочитанных студентами каждого факультета.
2 Топ-5 книг, которые выдавались наибольшему количеству разных
студентов.
3 Факультеты в порядке убывания количества доступных в данный
момент книг с учетом количества экземпляров каждой книги.
4 Список из 3 студентов, которые чаще других берут книги на своих
факультетов.
5 Список студентов по убыванию суммы трех самых дорогих книг,
которые они прочитали.
"""


import asyncio

from models import db
from models.model import Student, Book
from models.mock.books import create_books, create_faculty_books
from models.mock.students import create_students
from models.mock.faculty import create_faculties
from models.queries import (
    give_book_to_student, return_book, average_year_and_read_pages_per_faculty,
    get_most_popular_books, remain_books_by_faculty, most_well_read_by_faculty,
    most_expensive_books_by_student
)
from models.exceptions import BooksAreOverException, StudentAlreadyHaveBookException


async def main():
    db_uri = 'postgresql://danii:test@localhost/dansobolev'
    await db.set_bind(db_uri)
    await db.gino.create_all()

    # await create_faculties()
    # await create_books()
    # await create_students()
    # await create_faculty_books()

    # give book to student
    # student = await Student.get(1)
    # book = await Book.get(1)
    # try:
    #     await give_book_to_student(student, book)
    # except BooksAreOverException as e:
    #     print(e)
    # except StudentAlreadyHaveBookException as e:
    #     print(e)

    # take book from student
    # await return_book(student, book)

    # Task 3.1
    # print(await average_year_and_read_pages_per_faculty())

    # Task 3.2
    # TODO: test
    # print(await get_most_popular_books())

    # Task 3.3
    # TODO: test
    # print(await remain_books_by_faculty())

    # Task 3.4
    # TODO: test
    # print(await most_well_read_by_faculty())

    # Task 3.5
    # TODO: test
    # print(await most_expensive_books_by_student())

    await db.pop_bind().close()


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
