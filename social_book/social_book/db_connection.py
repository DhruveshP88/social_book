from sqlalchemy import create_engine
from sqlalchemy import text

def get_connection():
    engine = create_engine('postgresql://dhruvesh:hellow123@localhost/postgres')
    return engine.connect()

def fetch_books():
    with get_connection() as connection:
        # Explicitly reference the public schema
        result = connection.execute(text("SELECT * FROM public.books"))
        return result.fetchall()

# Call the function and print the results
books = fetch_books()
for book in books:
    print(book)
