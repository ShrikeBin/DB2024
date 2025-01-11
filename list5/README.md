# Dependencies
```bash 
pip install sqlalchemy
pip install bcrypt
pip install tkcalendar
sudo apt install python3-tk
```

### Tables are as follows:

#### User
- **id** (Integer) - Primary key, auto-incremented.
- **username** (String) - Unique, not nullable.
- **password_hash** (String) - Not nullable.
- **email** (String) - Unique, nullable.
- **role** (Enum) - Enum of `admin` or `librarian`, not nullable, default is `librarian`.
- **created_at** (DateTime) - Timestamp of when the user was created, default is the current UTC time.
- **updated_at** (DateTime) - Timestamp of when the user was last updated, default is the current UTC time, updates automatically on change.

#### Author
- **id** (Integer) - Primary key, auto-incremented.
- **name** (String) - Unique, not nullable.
- **birth_date** (Date) - Nullable.
- **biography** (Text) - Nullable.

#### Book
- **id** (Integer) - Primary key, auto-incremented.
- **title** (String) - Not nullable.
- **author_id** (Integer) - Foreign key to the `Author` table, not nullable.
- **published_date** (Date) - Nullable.
- **isbn** (String) - Unique, nullable.
- **available_copies** (Integer) - Not nullable, default is `1`.

#### Borrowing
- **id** (Integer) - Primary key, auto-incremented.
- **user_id** (Integer) - Foreign key to the `User` table, not nullable.
- **book_id** (Integer) - Foreign key to the `Book` table, not nullable.
- **borrowed_at** (DateTime) - Default is the current UTC time.
- **due_date** (DateTime) - Not nullable.
- **returned_at** (DateTime) - Nullable.

#### Category
- **id** (Integer) - Primary key, auto-incremented.
- **name** (String) - Unique, not nullable.
- **description** (Text) - Nullable.
- book_categories (sub-table)
- - **book_id** (Integer) - Foreign key to the `Book` table, primary key.
- - **category_id** (Integer) - Foreign key to the `Category` table, primary key.

#### Rating
- **id** (Integer) - Primary key, auto-incremented.
- **user_id** (Integer) - Foreign key to the `User` table, not nullable.
- **book_id** (Integer) - Foreign key to the `Book` table, not nullable.
- **rating** (Integer) - Not nullable.
- **review** (Text) - Nullable.
- **created_at** (DateTime) - Default is the current UTC time.

