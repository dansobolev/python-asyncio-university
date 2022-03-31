/* Разработать таблицы для хранения информации о книгах в библиотеке
(название, автор, год выпуска, количество страниц, количество
экземпляров) и данных о выданных книгах (кому, когда выдана, когда
возвращена)
Написать SQL запросы, позволяющие:
1 Добавить/удалить/изменить данные в таблице с книгами.
2 Посчитать количество выданных в данный момент книг.
3 Найти топ-3 книг, чаще всего выдаваемых на руки. */

create table if not exists book(
	id bigserial not null primary key,
	name text not null,
	author text,
	release_year integer,
	number_of_pages integer,
	number_of_copies integer
);

create table if not exists book_recipient(
	id bigserial not null primary key,
	recipient_name text not null,
	book_id integer not null references book(id),
	issue_date date not null,
	return_data date
);