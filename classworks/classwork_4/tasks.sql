/*
2. Посчитать количество выданных в данный момент книг.
*/

select count(*) from book_recipient where return_data is null;


/*
3 Найти топ-3 книг, чаще всего выдаваемых на руки.
*/

select count(book.id) as book_count, book.name
from book_recipient
join book on book_recipient.book_id = book.id
group by book.id
order by book_count desc
limit 3
