from sqlalchemy import Table, Column, Integer, String, ForeignKey, Date, Text, DateTime, Enum
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime
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
    
    borrowings = relationship('Borrowing', back_populates='user')
    ratings = relationship('Rating', back_populates='user')


class Author(Base):
    __tablename__ = 'authors'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)
    birth_date = Column(Date, nullable=True)
    biography = Column(Text, nullable=True)
    books = relationship('Book', back_populates='author')


class Book(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    author_id = Column(Integer, ForeignKey('authors.id'), nullable=False)
    published_date = Column(Date, nullable=True)
    isbn = Column(String, unique=True, nullable=True)
    available_copies = Column(Integer, nullable=False, default=1)
    author = relationship('Author', back_populates='books')
    categories = relationship('Category', secondary='book_categories', back_populates='books')
    borrowings = relationship('Borrowing', back_populates='book')
    ratings = relationship('Rating', back_populates='book')


class Borrowing(Base):
    __tablename__ = 'borrowings'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    book_id = Column(Integer, ForeignKey('books.id'), nullable=False)
    borrowed_at = Column(DateTime, default=datetime.utcnow)
    due_date = Column(DateTime, nullable=False)
    returned_at = Column(DateTime, nullable=True)
    user = relationship('User', back_populates='borrowings')
    book = relationship('Book', back_populates='borrowings')


class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(Text, nullable=True)
    books = relationship('Book', secondary='book_categories', back_populates='categories')


# Now define the many-to-many association table after the classes
book_categories = Table(
    'book_categories', Base.metadata,
    Column('book_id', Integer, ForeignKey('books.id'), primary_key=True),
    Column('category_id', Integer, ForeignKey('categories.id'), primary_key=True)
)


class Rating(Base):
    __tablename__ = 'ratings'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    book_id = Column(Integer, ForeignKey('books.id'), nullable=False)
    rating = Column(Integer, nullable=False)
    review = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    user = relationship('User', back_populates='ratings')
    book = relationship('Book', back_populates='ratings')
