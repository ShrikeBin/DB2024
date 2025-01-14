from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from models import Base

# Initialize database
# Set up the engine and session
engine = create_engine('sqlite:///library.db', echo=True)

Session = sessionmaker(bind=engine)

# Create tables
Base.metadata.create_all(engine)

# Global session instance
session = Session()


# Add triggers and pragmas
with engine.connect() as connection:
    connection.execute(text("""
        PRAGMA foreign_keys = ON;
    """))
    
    connection.execute(text("""
        CREATE TRIGGER IF NOT EXISTS new_copy
        AFTER INSERT ON books
        BEGIN
            UPDATE books
            SET available_copies = (
                SELECT available_copies + 1
                FROM books
                WHERE title = NEW.title AND author_id = NEW.author_id AND id != NEW.id
                LIMIT 1
            )
            WHERE id = NEW.id
            AND EXISTS (
                SELECT 1
                FROM books
                WHERE title = NEW.title AND author_id = NEW.author_id AND id != NEW.id
            );

            UPDATE books
            SET available_copies = 1
            WHERE id = NEW.id
            AND NOT EXISTS (
                SELECT 1
                FROM books
                WHERE title = NEW.title AND author_id = NEW.author_id AND id != NEW.id
            );
        END;
        """))
    
    connection.execute(text("""
        CREATE TRIGGER IF NOT EXISTS borrowed_book_nonavailable
        BEFORE INSERT ON borrowings
        BEGIN
            SELECT RAISE(ABORT, 'Book is not available')
            WHERE (SELECT available_copies FROM books WHERE id = NEW.book_id) <= 0;
                            
            UPDATE books
            SET available_copies = available_copies - 1
            WHERE id = NEW.book_id;
        END;
    """))

    connection.execute(text("""
        CREATE TRIGGER IF NOT EXISTS returned_book_available
        BEFORE UPDATE OF returned_at ON borrowings
        FOR EACH ROW
        WHEN NEW.returned_at IS NOT NULL AND OLD.returned_at IS NULL
        BEGIN
            UPDATE books
            SET available_copies = available_copies + 1
            WHERE id = NEW.book_id;
        END;
    """))
                            
    connection.execute(text("""
        CREATE TRIGGER IF NOT EXISTS prevent_borrowed_book_deletion
        BEFORE DELETE ON books
        BEGIN
            SELECT RAISE(ABORT, 'Cannot remove book that has been borrowed and not returned')
            WHERE EXISTS (
                SELECT 1 
                FROM borrowings 
                WHERE book_id = OLD.id AND returned_at IS NULL
            );
        END;
    """))
