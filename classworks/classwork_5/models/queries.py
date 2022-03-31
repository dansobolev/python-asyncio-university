import datetime
from typing import Union, Tuple, Dict, List
import statistics
import itertools

from sqlalchemy import and_

from models import db
from models.model import Book, Student, Faculty, StudentBook, FacultyBook
from models.exceptions import BooksAreOverException, StudentAlreadyHaveBookException


async def get_faculty(id_: Union[str, int]) -> Faculty:
    if isinstance(id_, int):
        return await Faculty.get(id_)
    elif isinstance(id_, str):
        return await Faculty.query.where(Faculty.name == id_).gino.first()


async def get_taken_books_quantity(book_id: int) -> int:
    """
    Функция возвращает количество экземпляров конкретной книги,
    которые в данный момент взяты из библиотеки.
    """
    quantity = await db.select([db.func.count()]).where(
        and_(StudentBook.return_date.is_(None), StudentBook.book_id == book_id)
    ).gino.scalar()
    return quantity


async def is_book_available(book: Book):
    quantity = await get_taken_books_quantity(book.id)
    if quantity != book.number_of_copies:
        return True


async def get_student_book(student: Student, book: Book) -> StudentBook:
    student_book = await StudentBook.query.where(and_(
        StudentBook.student_id == student.id,
        StudentBook.book_id == book.id,
        StudentBook.return_date.is_(None)
    )).gino.first()
    return student_book


async def get_student_books(student: Student, book: Book) -> List[StudentBook]:
    student_books = await StudentBook.query.where(and_(
        StudentBook.student_id == student.id,
        StudentBook.book_id == book.id
    )).gino.all()
    return student_books


async def is_student_have_book(student: Student, book: Book):
    student_books = await get_student_books(student, book)
    return_dates = [book.return_date for book in student_books]
    if not all(return_dates):
        return True


async def create_student(name: str, faculty_: str = 'ФИМП'):
    faculty = get_faculty(faculty_)
    student = Student(fio=name, faculty_id=faculty.id)
    await student.create()


async def create_book(name: str, release_year: int, **kwargs):
    book_data = {'name': name, 'release_year': release_year}
    if kwargs:
        book_data.update(kwargs)
    book = Book(**book_data)
    await book.create()


async def give_book_to_student(student: Student, book: Book):
    issue_date = datetime.date.today()
    is_book_available_ = await is_book_available(book)
    if not is_book_available_:
        raise BooksAreOverException("This type of book is over, sorry")
    is_student_have_book_ = await is_student_have_book(student, book)
    if is_student_have_book_:
        raise StudentAlreadyHaveBookException("This student is already have this book")
    student_book = StudentBook(book_id=book.id,
                               student_id=student.id,
                               issue_date=issue_date)
    await student_book.create()


async def return_book(student: Student, book: Book):
    student_book = await get_student_book(student, book)
    if student_book:
        await student_book.update(return_date=datetime.date.today()).apply()


async def average_year_and_read_pages_per_faculty() -> Dict[str, Dict[str, int]]:
    """
    Функция возвращает средний год издания книг и суммарное количество страниц,
    прочитанных студентами каждого факультета.
    """
    faculties = await Faculty.query.gino.all()
    faculties_d = {faculty: {} for faculty in faculties}
    for faculty_ in faculties_d.keys():
        students_faculty = await Student.query.where(Student.faculty_id == faculty_.id).gino.all()
        students_faculty_ids = [student.id for student in students_faculty]
        students_books = await StudentBook.query.where(and_(
            StudentBook.student_id.in_(students_faculty_ids),
            StudentBook.return_date != None)
        ).gino.all()
        books = await Book.query.where(Book.id.in_([book.book_id for book in students_books])).gino.all()
        pages = sum([book.number_of_pages for book in books])
        avg_year = statistics.mean([book.release_year for book in books]) if books else 0
        faculties_d[faculty_] = {'avg_year': avg_year, 'pages': pages}

    return {key.name: value for key, value in faculties_d.items()}


async def get_most_popular_books() -> Dict[int, int]:
    """
    Функция возвращает топ-5 книг, которые выдавались
    наибольшему количеству разных студентов.
    """
    student_books = await StudentBook.query.gino.all()
    books_d: Dict[int, List[int]] = {}
    for item in student_books:
        if item.book_id not in books_d:
            books_d[item.book_id] = [item.student_id]
        else:
            students = books_d[item.book_id]
            if item.student_id not in students:
                students.append(item.student_id)
                books_d.update({item.book_id: students})

    books_d: Dict[int, int] = {key: sum(value) for key, value in books_d.items()}
    books_sorted = dict(sorted(books_d.items(), key=lambda item_: item_[1], reverse=True))
    return dict(itertools.islice(books_sorted.items(), 5))


async def remain_books_by_faculty() -> List[Faculty]:
    """
    Функция возвращает факультеты в порядке убывания количества доступных в данный
    момент книг с учетом количества экземпляров каждой книги.
    """
    faculty_books = await FacultyBook.query.gino.all()
    faculties = {}
    for entry in faculty_books:
        book = await Book.get(entry.book_id)
        all_copies = book.number_of_copies
        remain_copies = all_copies - await get_taken_books_quantity(book.id)
        if entry.faculty_id not in faculties:
            faculties[entry.faculty_id] = remain_copies
        else:
            faculties[entry.faculty_id] += remain_copies
    sorted_ = dict(sorted(faculties.items(), key=lambda item_: item_[1], reverse=True))
    return sorted_


async def most_well_read_by_faculty() -> List[int]:
    """
    Функция возвращает список из 3 студентов, которые чаще
    других берут книги на своих факультетов.
    """
    student_books = await StudentBook.query.gino.all()
    faculties: Dict[int, Dict[int, int]] = {}
    students: Dict[int, int] = {}
    for entry in student_books:
        student = await Student.get(entry.student_id)
        faculty = student.faculty_id
        all_entries = await StudentBook.query.where(StudentBook.student_id == student.id).gino.all()
        students[student.id] = len(all_entries) if all_entries else 0
        faculties[faculty] = students

    most_well_read = {}
    for faculty, student_data in faculties.items():
        most_read_students = dict(sorted(student_data.items(), key=lambda item_: item_[1], reverse=True))
        # choose one most read student by each faculty
        most_read_student = dict(itertools.islice(most_read_students.items(), 1))
        # number of read book by most well read student
        most_well_read[faculty] = list(most_read_student.values())[0]

    most_read_students = dict(sorted(most_well_read.items(), key=lambda item_: item_[1], reverse=True))
    return list(dict(itertools.islice(most_read_students.items(), 3)).values())


async def most_expensive_books_by_student() -> Dict[int, int]:
    """
    Функция возвращает студентов по убыванию суммы трех самых дорогих книг,
    которые они прочитали.
    """
    student_books = await StudentBook.query.gino.all()
    books_d: Dict[int, List[int]] = {}
    for entry in student_books:
        if entry.student_id not in books_d:
            books_d[entry.student_id] = [entry.book_id]
        else:
            books = books_d[entry.student_id]
            books.append(entry.book_id)
            books_d.update({entry.student_id: books})

    for student, books in books_d.items():
        st_books = await Book.query.where(Book.id.in_(books)).gino.all()
        st_books = sorted([book.price for book in st_books], reverse=True)[:3]
        books_d.update({student: sum(st_books)})

    return books_d
