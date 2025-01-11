import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
from tkcalendar import DateEntry
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from models import Base, User, Book, Author, Category, Borrowing, Rating, UserRole
from functions import show_table_data, add_user, edit_user, delete_user, add_book, refresh_user_list, add_author, add_borrowing, add_category, add_rating
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
    table_window.geometry("1000x600")  # Increased width for separate sections

    # Function to go back to the main window
    def go_back():
        table_window.destroy()
        open_main_app(current_user)

    # Main frame to hold filter and checkbox sections
    main_frame = tk.Frame(table_window)
    main_frame.pack(fill=tk.BOTH, expand=True)

    # Frame for filtering options (left side)
    frame_filter = tk.Frame(main_frame)
    frame_filter.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=5)

    tk.Label(frame_filter, text="Filtr:").pack(anchor="w", padx=5)

    # Get model columns dynamically
    model = table_models.get(table)
    if not model:
        messagebox.showwarning("Error", "Model not found.")
        return
    
    model_columns = [column.name for column in model.__table__.columns]

    # Dropdown filter (Combobox) for columns
    filter_var = tk.StringVar()
    filter_dropdown = ttk.Combobox(frame_filter, textvariable=filter_var, values=model_columns, state="readonly")
    filter_dropdown.current(0)
    filter_dropdown.pack(anchor="w", padx=5, pady=2)

    # Entry for filter pattern with wildcards
    filter_entry = tk.Entry(frame_filter)
    filter_entry.pack(anchor="w", padx=5, pady=2)

    def apply_filter():
        selected_filter = filter_var.get()
        filter_value = filter_entry.get()
        query = session.query(model)
        if hasattr(model, selected_filter) and filter_value:
            query = query.filter(getattr(model, selected_filter).like(f"%{filter_value}%"))
        rows = query.all()
        selected_columns = [col for col, var in column_visibility.items() if var.get()]
        show_table_data(model, rows, listbox_data, session, selected_columns)

    tk.Button(frame_filter, text="Filtruj", command=apply_filter).pack(anchor="w", padx=5, pady=5)
    tk.Button(frame_filter, text="Wróc", command=go_back).pack(anchor="w", padx=5, pady=5)

    # Frame for checkbuttons (right side)
    frame_checkbuttons = tk.Frame(main_frame, relief=tk.GROOVE, bd=2)
    frame_checkbuttons.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=5)

    tk.Label(frame_checkbuttons, text="Pokaż kolumny:").pack(anchor="w", padx=5, pady=2)

    # Checkbuttons to toggle column visibility
    column_visibility = {col: tk.BooleanVar(value=True) for col in model_columns}

    def toggle_columns():
        selected_columns = [col for col, var in column_visibility.items() if var.get()]
        rows = session.query(model).all()
        show_table_data(model, rows, listbox_data, session, selected_columns)

    for col in model_columns:
        chk = ttk.Checkbutton(frame_checkbuttons, text=col, variable=column_visibility[col], command=toggle_columns)
        chk.pack(anchor="w", padx=5)

    # Frame for data display (center)
    frame_data_display = tk.Frame(main_frame)
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
    rows = session.query(model).all()
    show_table_data(model, rows, listbox_data, session, model_columns)

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

# Add Author
    frame_author = tk.Frame(root)
    frame_author.pack(padx=20, pady=10)

    label_author_name = tk.Label(frame_author, text="Imię i Nazwisko autora:")
    label_author_name.grid(row=0, column=0)

    entry_author_name = tk.Entry(frame_author)
    entry_author_name.grid(row=0, column=1)

    button_add_author = tk.Button(frame_author, text="Dodaj autora", command=lambda: add_author(entry_author_name, session))
    button_add_author.grid(row=1, columnspan=2)

    # Add Book
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

    # Add Borrowing
    frame_borrowing = tk.Frame(root)
    frame_borrowing.pack(padx=20, pady=10)

    label_borrowing_user = tk.Label(frame_borrowing, text="ID użytkownika:")
    label_borrowing_user.grid(row=0, column=0)

    entry_borrowing_user = tk.Entry(frame_borrowing)
    entry_borrowing_user.grid(row=0, column=1)

    label_borrowing_book = tk.Label(frame_borrowing, text="ID książki:")
    label_borrowing_book.grid(row=1, column=0)

    entry_borrowing_book = tk.Entry(frame_borrowing)
    entry_borrowing_book.grid(row=1, column=1)

    label_borrowing_due_date = tk.Label(frame_borrowing, text="Data zwrotu:")
    label_borrowing_due_date.grid(row=2, column=0)

    # Use DateEntry for date selection
    entry_borrowing_due_date = DateEntry(frame_borrowing, date_pattern='dd-mm-yyyy')  # Set the date format
    entry_borrowing_due_date.grid(row=2, column=1)

    button_add_borrowing = tk.Button(frame_borrowing, text="Dodaj wypożyczenie", command=lambda: add_borrowing(entry_borrowing_user, entry_borrowing_book, entry_borrowing_due_date, session))
    button_add_borrowing.grid(row=3, columnspan=2)

    # Add Category
    frame_category = tk.Frame(root)
    frame_category.pack(padx=20, pady=10)

    label_category_name = tk.Label(frame_category, text="Nazwa kategorii:")
    label_category_name.grid(row=0, column=0)

    entry_category_name = tk.Entry(frame_category)
    entry_category_name.grid(row=0, column=1)

    button_add_category = tk.Button(frame_category, text="Dodaj kategorię", command=lambda: add_category(entry_category_name, session))
    button_add_category.grid(row=1, columnspan=2)

    # Add Rating
    frame_rating = tk.Frame(root)
    frame_rating.pack(padx=20, pady=10)

    label_rating_user = tk.Label(frame_rating, text="ID użytkownika:")
    label_rating_user.grid(row=0, column=0)

    entry_rating_user = tk.Entry(frame_rating)
    entry_rating_user.grid(row=0, column=1)

    label_rating_book = tk.Label(frame_rating, text="ID książki:")
    label_rating_book.grid(row=1, column=0)

    entry_rating_book = tk.Entry(frame_rating)
    entry_rating_book.grid(row=1, column=1)

    label_rating_value = tk.Label(frame_rating, text="Ocena:")
    label_rating_value.grid(row=2, column=0)

    entry_rating_value = tk.Entry(frame_rating)
    entry_rating_value.grid(row=2, column=1)

    label_rating_review = tk.Label(frame_rating, text="Recenzja:")
    label_rating_review.grid(row=3, column=0)

    entry_rating_review = tk.Entry(frame_rating)
    entry_rating_review.grid(row=3, column=1)

    button_add_rating = tk.Button(frame_rating, text="Dodaj ocenę", command=lambda: add_rating(entry_rating_user, entry_rating_book, entry_rating_value, entry_rating_review, session))
    button_add_rating.grid(row=4, columnspan=2)

    
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
