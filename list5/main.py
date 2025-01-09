import tkinter as tk
from tkinter import messagebox, simpledialog
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from models import Base, User, Book, Author, Category, Borrowing, Rating
import bcrypt

# Inicjalizacja bazy danych
engine = create_engine('sqlite:///library.db')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

table_models = {
    "users": User,
    "books": Book,
    "authors": Author,
    "borrowings": Borrowing,
    "ratings": Rating,
    "categories": Category
}

# Funkcje do obsługi CRUD

def add_user():
    username = entry_username.get()
    password = entry_password.get()
    
    if not username or not password:
        messagebox.showwarning("Błąd", "Wszystkie pola muszą być wypełnione!")
        return
    
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    new_user = User(username=username, password_hash=hashed)
    
    try:
        session.add(new_user)
        session.commit()
        messagebox.showinfo("Sukces", "Użytkownik został dodany.")
        refresh_user_list()
    except IntegrityError:
        session.rollback()
        messagebox.showwarning("Błąd", "Użytkownik o tej nazwie już istnieje.")

def add_book():
    title = entry_book_title.get()
    author_name = entry_book_author.get()
    
    if not title or not author_name:
        messagebox.showwarning("Błąd", "Wszystkie pola muszą być wypełnione!")
        return
    
    # Dodaj autora, jeśli go nie ma
    author = session.query(Author).filter_by(name=author_name).first()
    if not author:
        author = Author(name=author_name)
        session.add(author)
        session.commit()

    new_book = Book(title=title, author_id=author.id)
    
    try:
        session.add(new_book)
        session.commit()
        messagebox.showinfo("Sukces", "Książka została dodana.")
        refresh_book_list()
    except IntegrityError:
        session.rollback()
        messagebox.showwarning("Błąd", "Wystąpił błąd przy dodawaniu książki.")

def edit_user():
    selected_user = listbox_users.curselection()
    if not selected_user:
        messagebox.showwarning("Błąd", "Proszę wybrać użytkownika.")
        return
    
    user_id = int(listbox_users.get(selected_user[0]).split(' - ')[0])  # Pobranie ID z listy
    user = session.query(User).filter_by(id=user_id).first()

    new_username = simpledialog.askstring("Edycja", "Nowa nazwa użytkownika:", initialvalue=user.username)
    if new_username:
        user.username = new_username
        session.commit()
        refresh_user_list()
        messagebox.showinfo("Sukces", "Użytkownik został zaktualizowany.")

def delete_user():
    selected_user = listbox_users.curselection()
    if not selected_user:
        messagebox.showwarning("Błąd", "Proszę wybrać użytkownika.")
        return
    
    user_id = int(listbox_users.get(selected_user[0]).split(' - ')[0])  # Pobranie ID z listy
    user = session.query(User).filter_by(id=user_id).first()
    
    try:
        session.delete(user)
        session.commit()
        refresh_user_list()
        messagebox.showinfo("Sukces", "Użytkownik został usunięty.")
    except:
        session.rollback()
        messagebox.showwarning("Błąd", "Wystąpił błąd przy usuwaniu użytkownika.")

def refresh_user_list():
    listbox_users.delete(0, tk.END)
    users = session.query(User).all()
    for user in users:
        listbox_users.insert(tk.END, f"{user.id} - {user.username}")

def refresh_book_list():
    listbox_books.delete(0, tk.END)
    books = session.query(Book).all()
    for book in books:
        listbox_books.insert(tk.END, f"{book.id} - {book.title}")

def search_books():
    search_query = entry_search.get()
    listbox_books.delete(0, tk.END)
    books = session.query(Book).filter(Book.title.like(f"%{search_query}%")).all()
    for book in books:
        listbox_books.insert(tk.END, f"{book.id} - {book.title}")

# Funkcja do bezpiecznego tworzenia zapytań SQL
def safe_query(query, params=None):
    try:
        if params:
            return session.execute(query, params).fetchall()
        return session.execute(query).fetchall()
    except Exception as e:
        messagebox.showerror("Błąd zapytania", str(e))

def show_table_data(model, rows):
    # Wyczyść listbox przed dodaniem nowych danych
    listbox_data.delete(0, tk.END)

    # Wstaw dane do listboxa
    for row in rows:
        # Sprawdzamy, które kolumny należy wyświetlić
        row_data = ", ".join([f"{column.name}: {getattr(row, column.name)}" for column in model.__table__.columns])
        listbox_data.insert(tk.END, row_data)


def go_back_to_main():
    frame_data.pack_forget()
    frame_main.pack(padx=20, pady=10)

def enter_table(table):
    # Ukryj główny ekran
    frame_main.pack_forget()
    # Pokaż ekran z danymi
    frame_data.pack(padx=20, pady=10)
    label_table_name.config(text=f"Zawartość tabeli: {table.capitalize()}")
    
    # Sprawdzamy, czy tabela zawiera dane, zanim wyświetlimy je
    model = table_models.get(table)
    
    if model:
        rows = session.query(model).all()
        
        # Sprawdzamy, czy tabela jest pusta
        if not rows:
            listbox_data.delete(0, tk.END)
            listbox_data.insert(tk.END, "Tabela jest pusta.")
        else:
            show_table_data(model, rows)



# Tworzenie GUI
root = tk.Tk()
root.title("Biblioteka")

# Sekcja dla użytkowników
frame_user = tk.Frame(root)
frame_user.pack(padx=20, pady=10)

label_username = tk.Label(frame_user, text="Nazwa użytkownika:")
label_username.grid(row=0, column=0)

entry_username = tk.Entry(frame_user)
entry_username.grid(row=0, column=1)

label_password = tk.Label(frame_user, text="Hasło:")
label_password.grid(row=1, column=0)

entry_password = tk.Entry(frame_user, show="*")
entry_password.grid(row=1, column=1)

button_add_user = tk.Button(frame_user, text="Dodaj użytkownika", command=add_user)
button_add_user.grid(row=2, columnspan=2)

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

button_add_book = tk.Button(frame_book, text="Dodaj książkę", command=add_book)
button_add_book.grid(row=2, columnspan=2)

# Lista użytkowników
frame_user_list = tk.Frame(root)
frame_user_list.pack(padx=20, pady=10)

label_users = tk.Label(frame_user_list, text="Użytkownicy:")
label_users.grid(row=0, column=0)

listbox_users = tk.Listbox(frame_user_list)
listbox_users.grid(row=1, column=0)

button_edit_user = tk.Button(frame_user_list, text="Edytuj użytkownika", command=edit_user)
button_edit_user.grid(row=2, columnspan=2)

button_delete_user = tk.Button(frame_user_list, text="Usuń użytkownika", command=delete_user)
button_delete_user.grid(row=3, columnspan=2)

# Strona główna - wybór tabeli
frame_main = tk.Frame(root)
frame_main.pack(padx=20, pady=10)

label_main = tk.Label(frame_main, text="Wybierz tabelę do przeglądania:")
label_main.pack()

button_users = tk.Button(frame_main, text="Użytkownicy", command=lambda: enter_table("users"))
button_users.pack()

button_books = tk.Button(frame_main, text="Książki", command=lambda: enter_table("books"))
button_books.pack()

button_authors = tk.Button(frame_main, text="Autorzy", command=lambda: enter_table("authors"))
button_authors.pack()

button_borrowings = tk.Button(frame_main, text="Wypożyczenia", command=lambda: enter_table("borrowings"))
button_borrowings.pack()

button_ratings = tk.Button(frame_main, text="Oceny", command=lambda: enter_table("ratings"))
button_ratings.pack()

button_categories = tk.Button(frame_main, text="Kategorie", command=lambda: enter_table("categories"))
button_categories.pack()

# Strona z danymi tabeli
frame_data = tk.Frame(root)

label_table_name = tk.Label(frame_data, text="")
label_table_name.pack()

listbox_data = tk.Listbox(frame_data)
listbox_data.pack()

button_back = tk.Button(frame_data, text="Wróć", command=go_back_to_main)
button_back.pack()

frame_data_listbox = tk.Frame(frame_data)
frame_data_listbox.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)

listbox_data = tk.Listbox(frame_data_listbox, height=15, width=100)
listbox_data.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar_y = tk.Scrollbar(frame_data_listbox, orient="vertical", command=listbox_data.yview)
scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)

scrollbar_x = tk.Scrollbar(frame_data_listbox, orient="vertical", command=listbox_data.xview)
scrollbar_x.pack(side=tk.LEFT, fill=tk.X)

listbox_data.config(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)


root.mainloop()
