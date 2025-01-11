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

def refresh_user_list(listbox_users, session):
    listbox_users.delete(0, tk.END)
    users = session.query(User).all()
    for user in users:
        listbox_users.insert(tk.END, f"{user.id} - {user.username}")
        
def show_table_data(model, rows, listbox_data, session):
# Wyczyść listbox przed dodaniem nowych danych
    listbox_data.delete(0, tk.END)

    # Wstaw dane do listboxa
    for row in rows:
        # Sprawdzamy, które kolumny należy wyświetlić
        row_data = ", ".join([f"{column.name}: {getattr(row, column.name)}" for column in model.__table__.columns])
        listbox_data.insert(tk.END, row_data)        