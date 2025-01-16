import tkinter as tk
from tkinter import messagebox, simpledialog
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from models import Base, User, Book, Author, Category, Borrowing, Rating, UserRole
import bcrypt

# CRUD Functions
def add_user(entry_username, entry_password, listbox_users ,session):
    username = entry_username.get()
    password = entry_password.get()
    
    if not username or not password:
        messagebox.showwarning("Error", "All fields must be filled!")
        return
    
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    new_user = User(username=username, password_hash=hashed)
    
    try:
        session.add(new_user)
        session.commit()
        messagebox.showinfo("Success", "User added.")
        refresh_user_list(listbox_users, session)
    except IntegrityError:
        session.rollback()
        messagebox.showwarning("Error", "User already exists.")

def add_book(entry_book_title, entry_book_author, session):
    title = entry_book_title.get()
    author_name = entry_book_author.get()
    
    if not title or not author_name:
        messagebox.showwarning("Error", "All fields must be filled!")
        return
    
    author = session.query(Author).filter_by(name=author_name).first()
    if not author:
        author = Author(name=author_name)
        session.add(author)
        session.commit()

    new_book = Book(title=title, author_id=author.id)
    
    try:
        session.add(new_book)
        session.commit()
        messagebox.showinfo("Success", "Book added.")
    except IntegrityError:
        session.rollback()
        messagebox.showwarning("Error", "Error adding book.")

def edit_user(listbox_users, session):
    selected_user = listbox_users.curselection()
    if not selected_user:
        messagebox.showwarning("Error", "Select a user.")
        return

    user_id = int(listbox_users.get(selected_user[0]).split(' - ')[0])
    user = session.query(User).filter_by(id=user_id).first()
    print(user)

    # Prompt for a new username
    new_username = simpledialog.askstring("Edit", "New username:", initialvalue=user.username)
    if new_username:
        user.username = new_username

        # Prompt for a new password
        new_password = simpledialog.askstring("Edit", "New password (leave empty to keep current):", show="*")
        if new_password:
            hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
            user.password_hash = hashed_password

        session.commit()
        refresh_user_list(listbox_users, session)
        messagebox.showinfo("Success", "User updated.")


def delete_user(current_user, listbox_users, session):
    selected_user = listbox_users.curselection()
    if not selected_user:
        messagebox.showwarning("Error", "Select a user.")
        return
    
    user_id = int(listbox_users.get(selected_user[0]).split(' - ')[0])
    
    if user_id == current_user.id:
        messagebox.showwarning("Error", "You cannot delete your own account.")
        return
    
    user = session.query(User).filter_by(id=user_id).first()
    
    try:
        session.delete(user)
        session.commit()
        refresh_user_list(listbox_users, session)
        messagebox.showinfo("Success", "User deleted.")
    except:
        session.rollback()
        messagebox.showwarning("Error", "Error deleting user.")
        
def add_author(entry_author_name, session):
    author_name = entry_author_name.get()
    
    if not author_name:
        messagebox.showwarning("Error", "Author name must be filled!")
        return
    
    new_author = Author(name=author_name)
    
    try:
        session.add(new_author)
        session.commit()
        messagebox.showinfo("Success", "Author added.")
    except IntegrityError:
        session.rollback()
        messagebox.showwarning("Error", "Error adding author.")

from datetime import datetime

# Add Borrowing
def add_borrowing(entry_borrowing_user, entry_borrowing_book, entry_borrowing_due_date, session):
    user_id = entry_borrowing_user.get()
    book_id = entry_borrowing_book.get()
    due_date_str = entry_borrowing_due_date.get()  # This is a string in 'yyyy-mm-dd' format

    # Convert due_date string to datetime object
    try:
        due_date = datetime.strptime(due_date_str, '%d-%m-%Y')  # Convert to datetime object
    except ValueError:
        messagebox.showwarning("Error", "Invalid date format.")
        return

    # Ensure that the user_id and book_id are integers
    try:
        user_id = int(user_id)
        book_id = int(book_id)
    except ValueError:
        messagebox.showwarning("Error", "User ID and Book ID must be integers.")
        return
    
    # Create a new Borrowing object
    new_borrowing = Borrowing(user_id=user_id, book_id=book_id, due_date=due_date, returned_at=None)

    try:
        session.add(new_borrowing)
        session.commit()
        messagebox.showinfo("Success", "Borrowing added.")
    except Exception as e:
        session.rollback()
        messagebox.showwarning("Error", f"Error adding borrowing: {str(e)}")


def add_category(entry_category_name, session):
    category_name = entry_category_name.get()
    
    if not category_name:
        messagebox.showwarning("Error", "Category name must be filled!")
        return
    
    new_category = Category(name=category_name)
    
    try:
        session.add(new_category)
        session.commit()
        messagebox.showinfo("Success", "Category added.")
    except IntegrityError:
        session.rollback()
        messagebox.showwarning("Error", "Error adding category.")

def add_rating(entry_rating_user, entry_rating_book, entry_rating_value, entry_rating_review, session):
    user_id = entry_rating_user.get()
    book_id = entry_rating_book.get()
    rating_value = entry_rating_value.get()
    review = entry_rating_review.get()
    
    if not user_id or not book_id or not rating_value:
        messagebox.showwarning("Error", "User ID, Book ID, and Rating are required!")
        return
    
    try:
        user_id = int(user_id)
        book_id = int(book_id)
        rating_value = int(rating_value)
    except ValueError:
        messagebox.showwarning("Error", "User ID, Book ID, and Rating must be integers!")
        return

    if rating_value < 1 or rating_value > 5:
        messagebox.showwarning("Error", "Rating must be between 1 and 5!")
        return
    
    user = session.query(User).filter_by(id=user_id).first()
    book = session.query(Book).filter_by(id=book_id).first()
    
    if not user or not book:
        messagebox.showwarning("Error", "User or Book not found!")
        return

    new_rating = Rating(user_id=user_id, book_id=book_id, rating=rating_value, review=review)
    
    try:
        session.add(new_rating)
        session.commit()
        messagebox.showinfo("Success", "Rating added.")
    except IntegrityError:
        session.rollback()
        messagebox.showwarning("Error", "Error adding rating.")


def refresh_user_list(listbox_users, session):
    listbox_users.delete(0, tk.END)
    users = session.query(User).all()
    for user in users:
        listbox_users.insert(tk.END, f"{user.id} - {user.username}")
        
def show_table_data(model, rows, listbox_data, session, selected_columns):
    # Clear the listbox before adding new data
    listbox_data.delete(0, tk.END)

    # Insert data into the listbox based on selected columns
    for row in rows:
        row_data = ", ".join([f"{col}: {getattr(row, col)}" for col in selected_columns])
        listbox_data.insert(tk.END, row_data)
