from db_connection import get_connection
from sqlalchemy import text

def fetch_books():
    with get_connection() as connection:
        result = connection.execute(text("SELECT * FROM books"))
        return result.fetchall()

# Call the function and print the results
books = fetch_books()
for book in books:
    print(book)
