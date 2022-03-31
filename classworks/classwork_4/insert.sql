insert into book(name, author, release_year, number_of_pages, number_of_copies)
values
	('1984', 'Джордж Оруэлл', 1949, 328, 5),
	('Раковый корпус', 'А. Солженицын', 1966, 438, 3),
	('Book 1', 'Author 1', 2000, 532, 2),
    ('Book 2', 'Author 2', 1998, 731, 3);

insert into book_recipient(recipient_name, book_id, issue_date, return_data)
values
    ('Daniil', 1, '2022-02-25', null),
    ('Artem', 2, '2022-01-19', null),
    ('Maria', 3, '2021-12-01', '2022-02-25'),
    ('Name 1', 2, '2022-01-18', null),
    ('Name 2', 2, '2022-01-18', null),
    ('Name 3', 1, '2021-05-12', '2021-06-15'),
    ('Name 4', 4, '2021-06-13', '2021-06-28'),
    ('Name 5', 4, '2021-01-12', '2021-02-15');