
SELECT books.id, books.title, books.path, books.isbn, authors.name
FROM books, books_authors_link, authors
WHERE books_authors_link.book = books.id
AND books_authors_link.author = authors.id;

