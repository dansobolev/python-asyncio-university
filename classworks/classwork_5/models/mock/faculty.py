from models.model import Faculty


faculties = (
    ('ФИПМ', ),
    ('Менеджмент', ),
    ('Иностранные языки', ),
)

columns_names = ['name']


async def create_faculties():
    for faculty_ in faculties:
        faculty_data = {key: value for key, value in zip(columns_names, faculty_)}
        faculty = Faculty(**faculty_data)
        await faculty.create()
