from models.model import Book, FacultyBook

books = (
    ('1984', 1949, 328, 100, 5),
 	('Раковый корпус', 1966, 438, 250, 3),
 	('Book 1', 2000, 532, 125, 2),
    ('Book 2', 1998, 731, 378, 3),
)

column_names = ['name', 'release_year', 'number_of_pages',
                'price', 'number_of_copies']


async def create_books():
    for book_ in books:
        book_data = {key: value for key, value in zip(column_names, book_)}
        book = Book(**book_data)
        await book.create()


async def create_faculty_books():
    pairs = ((1, 1), (1, 2), (2, 1), (3, 1), (1, 3))
    for pair in pairs:
        dict_ = {'book_id': pair[0], 'faculty_id': pair[1]}
        faculty_book = FacultyBook(**dict_)
        await faculty_book.create()
