import tkinter as tk
from tkinter import messagebox, simpledialog
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from models import Base, User, Book, Author, Category, Borrowing, Rating, UserRole
from functions import show_table_data, add_user, edit_user, delete_user, add_book, refresh_user_list
import bcrypt

# Initialize database
engine = create_engine('sqlite:///library.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

# Mapping table models
table_models = {
    "users": User,
    "books": Book,
    "authors": Author,
    "borrowings": Borrowing,
    "ratings": Rating,
    "categories": Category
}

# Default admin creation
if not session.query(User).first():
    hashed = bcrypt.hashpw("admin".encode('utf-8'), bcrypt.gensalt())
    default_admin = User(username="admin", password_hash=hashed, role=UserRole.ADMIN)
    session.add(default_admin)
    session.commit()



# Login Function
def login(login_window, entry_login_username, entry_login_password): #????
    username = entry_login_username.get()
    password = entry_login_password.get()

    user = session.query(User).filter_by(username=username).first()
    if user and bcrypt.checkpw(password.encode('utf-8'), user.password_hash):
        login_window.destroy()
        open_main_app(user)
    else:
        messagebox.showerror("Login Error", "Invalid username or password.")       
              
def enter_table(table, root, current_user):
    # Close the previous window
    root.destroy()
    
    # Create a new window
    table_window = tk.Tk()
    table_window.title(f"Table: {table.capitalize()}")
    table_window.geometry("800x600")

    # Function to go back to the main window
    def go_back():
        table_window.destroy()
        open_main_app(current_user)  # Reopen the main window

    # Frame for filtering options
    frame_filter = tk.Frame(table_window)
    frame_filter.pack(fill=tk.X, padx=10, pady=5)

    tk.Label(frame_filter, text="Filtr:").pack(side=tk.LEFT, padx=5)

    filter_entry = tk.Entry(frame_filter)
    filter_entry.pack(side=tk.LEFT, padx=5)

    def apply_filter():
        filter_value = filter_entry.get()
        model = table_models.get(table)
        if model:
            if filter_value:
                rows = session.query(model).filter(
                    model.title.like(f"%{filter_value}%") if hasattr(model, 'title') else model.username.like(f"%{filter_value}%")
                ).all()
            else:
                rows = session.query(model).all()
            show_table_data(model, rows, listbox_data)

    tk.Button(frame_filter, text="Filtruj", command=apply_filter).pack(side=tk.LEFT, padx=5)
    tk.Button(frame_filter, text="Wróc", command=go_back).pack(side=tk.RIGHT, padx=5)

    # Frame for data display with scrollbars
    frame_data_display = tk.Frame(table_window)
    frame_data_display.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    scrollbar_y = tk.Scrollbar(frame_data_display, orient=tk.VERTICAL)
    scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)

    scrollbar_x = tk.Scrollbar(frame_data_display, orient=tk.HORIZONTAL)
    scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)

    listbox_data = tk.Listbox(frame_data_display, yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set, width=100, height=30)
    listbox_data.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    scrollbar_y.config(command=listbox_data.yview)
    scrollbar_x.config(command=listbox_data.xview)

    # Load initial data
    model = table_models.get(table)
    if model:
        rows = session.query(model).all()
        show_table_data(model, rows, listbox_data, session)

    table_window.mainloop()

# Open main application
def open_main_app(current_user):
    root = tk.Tk()
    root.title("Zarządzanie Biblioteką")
    
    def is_admin():
        return current_user.role == UserRole.ADMIN

    # User management section (Admin only)
    if is_admin():
        global entry_username, entry_password, listbox_users
        frame_user = tk.Frame(root)
        frame_user.pack(padx=20, pady=10)

        tk.Label(frame_user, text="Username:").grid(row=0, column=0)
        entry_username = tk.Entry(frame_user)
        entry_username.grid(row=0, column=1)

        tk.Label(frame_user, text="Password:").grid(row=1, column=0)
        entry_password = tk.Entry(frame_user, show="*")
        entry_password.grid(row=1, column=1)

        listbox_users = tk.Listbox(frame_user)
        listbox_users.grid(row=3, columnspan=2)
        refresh_user_list(listbox_users, session)
        
        tk.Button(frame_user, text="Add User", command=lambda: add_user(entry_username, entry_password, listbox_users, session)).grid(row=2, columnspan=2)
        
        button_edit_user = tk.Button(frame_user, text="Edytuj użytkownika", command=lambda: edit_user(listbox_users, session))
        button_edit_user.grid(row=4, columnspan=2)

        button_delete_user = tk.Button(frame_user, text="Usuń użytkownika", command=lambda: delete_user(current_user, listbox_users, session))
        button_delete_user.grid(row=5, columnspan=2)

    # Sekcja dla książek
    frame_book = tk.Frame(root)
    frame_book.pack(padx=20, pady=10)

    label_book_title = tk.Label(frame_book, text="Tytuł książki:")
    label_book_title.grid(row=0, column=0)

    entry_book_title = tk.Entry(frame_book)
    entry_book_title.grid(row=0, column=1)

    label_book_author = tk.Label(frame_book, text="Autor książki:")
    label_book_author.grid(row=1, column=0)

    entry_book_author = tk.Entry(frame_book)
    entry_book_author.grid(row=1, column=1)

    button_add_book = tk.Button(frame_book, text="Dodaj książkę", command=lambda: add_book(entry_book_title, entry_book_author, session))
    button_add_book.grid(row=2, columnspan=2)

    
    # Strona główna - wybór tabeli
    frame_main = tk.Frame(root)
    frame_main.pack(padx=20, pady=10)

    label_main = tk.Label(frame_main, text="Wybierz tabelę do przeglądania:")
    label_main.pack()

    button_users = tk.Button(frame_main, text="Użytkownicy", command=lambda: enter_table("users", root, current_user))
    button_users.pack()

    button_books = tk.Button(frame_main, text="Książki", command=lambda: enter_table("books", root, current_user))
    button_books.pack()

    button_authors = tk.Button(frame_main, text="Autorzy", command=lambda: enter_table("authors", root, current_user))
    button_authors.pack()

    button_borrowings = tk.Button(frame_main, text="Wypożyczenia", command=lambda: enter_table("borrowings", root, current_user))
    button_borrowings.pack()

    button_ratings = tk.Button(frame_main, text="Oceny", command=lambda: enter_table("ratings", root, current_user))
    button_ratings.pack()

    button_categories = tk.Button(frame_main, text="Kategorie", command=lambda: enter_table("categories", root, current_user))
    button_categories.pack()

    root.mainloop()
