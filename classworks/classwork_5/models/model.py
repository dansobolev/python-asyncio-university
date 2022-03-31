from sqlalchemy import func
from . import db


class TimestampMixin(db.Model):
    __abstract__ = True

    created_at = db.Column('created_at', db.DateTime, server_default=func.now(),
                           nullable=False, doc='Время создания объекта')
    updated_at = db.Column('updated_at', db.DateTime, server_default=func.now(),
                           onupdate=func.now(), nullable=False,
                           doc='Время обновления объекта')


class Book(TimestampMixin):
    __tablename__ = 'book'

    id = db.Column('id', db.Integer, primary_key=True, nullable=False)
    name = db.Column('name', db.String, nullable=False)
    release_year = db.Column('release_year', db.Integer, nullable=False)
    number_of_pages = db.Column('number_of_pages', db.Integer, nullable=False)
    price = db.Column('price', db.Integer, nullable=False)
    number_of_copies = db.Column('number_of_copies', db.Integer, nullable=False)


class Student(TimestampMixin):
    __tablename__ = 'student'

    id = db.Column('id', db.Integer, primary_key=True, nullable=False)
    fio = db.Column('fio', db.String, nullable=False)
    faculty_id = db.Column('faculty_id', db.Integer,
                           db.ForeignKey('faculty.id'), nullable=False)


class Faculty(TimestampMixin):
    __tablename__ = 'faculty'

    id = db.Column('id', db.Integer, primary_key=True, nullable=False)
    name = db.Column('name', db.String, nullable=False)


class StudentBook(TimestampMixin):
    __tablename__ = 'student_book'

    id = db.Column('id', db.Integer, primary_key=True, nullable=False)
    book_id = db.Column('book_id', db.Integer,
                        db.ForeignKey('book.id'), nullable=False)
    student_id = db.Column('student_id', db.Integer,
                           db.ForeignKey('student.id'), nullable=False)
    issue_date = db.Column('issue_date', db.Date, nullable=False,
                           doc='Дата взятия книги из библиотеки')
    return_date = db.Column('return_date', db.Date,
                            doc='Дата возарата книги в библиотеку')


class FacultyBook(TimestampMixin):
    __tablename__ = 'faculty_book'

    id = db.Column('id', db.Integer, primary_key=True, nullable=False)
    book_id = db.Column('book_id', db.Integer,
                        db.ForeignKey('book.id'), nullable=False)
    faculty_id = db.Column('faculty_id', db.Integer,
                           db.ForeignKey('faculty.id'), nullable=False)
