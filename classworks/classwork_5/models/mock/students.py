from models.model import Student


students = (
    ('student 1', 1),
    ('student 2', 1),
    ('student 3', 1),
    ('student 4', 2),
    ('student 5', 2),
)

columns_names = ['fio', 'faculty_id']


async def create_students():
    for student_ in students:
        student_data = {key: value for key, value in zip(columns_names, student_)}
        student = Student(**student_data)
        await student.create()
