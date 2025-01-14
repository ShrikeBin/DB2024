from sqlalchemy import Table, Column, Integer, String, ForeignKey, Date, Text, DateTime, Enum
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime, timedelta
import enum

# Define your models first

Base = declarative_base()

class UserRole(enum.Enum):
    ADMIN = "admin"
    LIBRARIAN = "librarian"

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=True)
    role = Column(Enum(UserRole), nullable=False, default=UserRole.LIBRARIAN)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Author(Base):
    __tablename__ = 'authors'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)
    birth_date = Column(Date, nullable=True)
    biography = Column(Text, nullable=True)

    __editable_columns__ = ['name', 'birth_date', 'biography']


class Book(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    author_id = Column(Integer, ForeignKey('authors.id'), nullable=False)
    published_date = Column(Date, nullable=True)
    isbn = Column(String, unique=True, nullable=True)
    available_copies = Column(Integer, nullable=False, default=1)

    __editable_columns__ = ['title', 'author_id', 'published_date', 'isbn']


class Borrowing(Base):
    __tablename__ = 'borrowings'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    book_id = Column(Integer, ForeignKey('books.id'), nullable=False)
    borrowed_at = Column(DateTime, default=datetime.utcnow)
    due_date = Column(DateTime, nullable=False, default=lambda: datetime.utcnow() + timedelta(days=30))
    returned_at = Column(DateTime, nullable=True)

    __editable_columns__ = ['user_id', 'book_id']


class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(Text, nullable=True)

    __editable_columns__ = ['name', 'description']


class BookCategory(Base):
    __tablename__ = 'book_categories'

    id = Column(Integer, primary_key=True, autoincrement=True)
    book_id = Column(Integer, ForeignKey('books.id'), nullable=False)
    category_id = Column(Integer, ForeignKey('categories.id'), nullable=False)

    __editable_columns__ = ['book_id', 'category_id']


class Rating(Base):
    __tablename__ = 'ratings'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    book_id = Column(Integer, ForeignKey('books.id'), nullable=False)
    rating = Column(Integer, nullable=False)
    review = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    __editable_columns__ = ['user_id', 'book_id', 'rating', 'review']
