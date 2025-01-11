#include <iostream>
#include <sqlite3.h>
#include <string>
#include <sstream>

using namespace std;

// Callback function to handle SQL execution results
int callback(void* data, int argc, char** argv, char** colnames) {
    for (int i = 0; i < argc; i++) {
        cout << colnames[i] << " = " << (argv[i] ? argv[i] : "NULL") << endl;
    }
    return 0;
}

class DatabaseManager {
private:
    sqlite3* db;

public:
    DatabaseManager(const string& db_name) {
        if (sqlite3_open(db_name.c_str(), &db)) {
            cerr << "Can't open database: " << sqlite3_errmsg(db) << endl;
            return;
        }
        cout << "Opened database successfully\n";
    }

    ~DatabaseManager() {
        sqlite3_close(db);
    }

    // Create tables
    void createTables() {
        const char* create_users_table = R"(
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                email TEXT UNIQUE,
                role TEXT NOT NULL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT DEFAULT CURRENT_TIMESTAMP
            );
        )";

        const char* create_authors_table = R"(
            CREATE TABLE IF NOT EXISTS authors (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                birth_date TEXT,
                biography TEXT
            );
        )";

        const char* create_books_table = R"(
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                author_id INTEGER,
                published_date TEXT,
                isbn TEXT UNIQUE,
                available_copies INTEGER DEFAULT 1,
                FOREIGN KEY (author_id) REFERENCES authors (id)
            );
        )";

        const char* create_borrowings_table = R"(
            CREATE TABLE IF NOT EXISTS borrowings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                book_id INTEGER NOT NULL,
                borrowed_at TEXT DEFAULT CURRENT_TIMESTAMP,
                due_date TEXT NOT NULL,
                returned_at TEXT,
                FOREIGN KEY (user_id) REFERENCES users (id),
                FOREIGN KEY (book_id) REFERENCES books (id)
            );
        )";

        const char* create_categories_table = R"(
            CREATE TABLE IF NOT EXISTS categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                description TEXT
            );
        )";

        const char* create_ratings_table = R"(
            CREATE TABLE IF NOT EXISTS ratings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                book_id INTEGER NOT NULL,
                rating INTEGER NOT NULL,
                review TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id),
                FOREIGN KEY (book_id) REFERENCES books (id)
            );
        )";

        char* errMsg = nullptr;

        // Execute SQL queries to create tables
        if (sqlite3_exec(db, create_users_table, callback, nullptr, &errMsg) != SQLITE_OK) {
            cerr << "SQL error: " << errMsg << endl;
            sqlite3_free(errMsg);
        }

        if (sqlite3_exec(db, create_authors_table, callback, nullptr, &errMsg) != SQLITE_OK) {
            cerr << "SQL error: " << errMsg << endl;
            sqlite3_free(errMsg);
        }

        if (sqlite3_exec(db, create_books_table, callback, nullptr, &errMsg) != SQLITE_OK) {
            cerr << "SQL error: " << errMsg << endl;
            sqlite3_free(errMsg);
        }

        if (sqlite3_exec(db, create_borrowings_table, callback, nullptr, &errMsg) != SQLITE_OK) {
            cerr << "SQL error: " << errMsg << endl;
            sqlite3_free(errMsg);
        }

        if (sqlite3_exec(db, create_categories_table, callback, nullptr, &errMsg) != SQLITE_OK) {
            cerr << "SQL error: " << errMsg << endl;
            sqlite3_free(errMsg);
        }

        if (sqlite3_exec(db, create_ratings_table, callback, nullptr, &errMsg) != SQLITE_OK) {
            cerr << "SQL error: " << errMsg << endl;
            sqlite3_free(errMsg);
        }

        cout << "Tables created successfully\n";
    }

    // Function to insert a user into the database
    void addUser(const string& username, const string& password_hash, const string& email, const string& role) {
        stringstream sql;
        sql << "INSERT INTO users (username, password_hash, email, role) VALUES ('" 
            << username << "', '" 
            << password_hash << "', '" 
            << email << "', '" 
            << role << "');";

        char* errMsg = nullptr;
        if (sqlite3_exec(db, sql.str().c_str(), callback, nullptr, &errMsg) != SQLITE_OK) {
            cerr << "SQL error: " << errMsg << endl;
            sqlite3_free(errMsg);
        } else {
            cout << "User added successfully\n";
        }
    }

    // Function to insert an author into the database
    void addAuthor(const string& name, const string& birth_date, const string& biography) {
        stringstream sql;
        sql << "INSERT INTO authors (name, birth_date, biography) VALUES ('"
            << name << "', '"
            << birth_date << "', '"
            << biography << "');";

        char* errMsg = nullptr;
        if (sqlite3_exec(db, sql.str().c_str(), callback, nullptr, &errMsg) != SQLITE_OK) {
            cerr << "SQL error: " << errMsg << endl;
            sqlite3_free(errMsg);
        } else {
            cout << "Author added successfully\n";
        }
    }

    // Function to insert a book into the database
    void addBook(const string& title, int author_id, const string& published_date, const string& isbn, int available_copies) {
        stringstream sql;
        sql << "INSERT INTO books (title, author_id, published_date, isbn, available_copies) VALUES ('"
            << title << "', "
            << author_id << ", '"
            << published_date << "', '"
            << isbn << "', "
            << available_copies << ");";

        char* errMsg = nullptr;
        if (sqlite3_exec(db, sql.str().c_str(), callback, nullptr, &errMsg) != SQLITE_OK) {
            cerr << "SQL error: " << errMsg << endl;
            sqlite3_free(errMsg);
        } else {
            cout << "Book added successfully\n";
        }
    }

    // Function to insert a borrowing into the database
    void addBorrowing(int user_id, int book_id, const string& due_date) {
        stringstream sql;
        sql << "INSERT INTO borrowings (user_id, book_id, due_date) VALUES ("
            << user_id << ", "
            << book_id << ", '"
            << due_date << "');";

        char* errMsg = nullptr;
        if (sqlite3_exec(db, sql.str().c_str(), callback, nullptr, &errMsg) != SQLITE_OK) {
            cerr << "SQL error: " << errMsg << endl;
            sqlite3_free(errMsg);
        } else {
            cout << "Borrowing added successfully\n";
        }
    }

    // Function to insert a category into the database
    void addCategory(const string& name, const string& description) {
        stringstream sql;
        sql << "INSERT INTO categories (name, description) VALUES ('"
            << name << "', '"
            << description << "');";

        char* errMsg = nullptr;
        if (sqlite3_exec(db, sql.str().c_str(), callback, nullptr, &errMsg) != SQLITE_OK) {
            cerr << "SQL error: " << errMsg << endl;
            sqlite3_free(errMsg);
        } else {
            cout << "Category added successfully\n";
        }
    }

    // Function to insert a rating into the database
    void addRating(int user_id, int book_id, int rating, const string& review) {
        stringstream sql;
        sql << "INSERT INTO ratings (user_id, book_id, rating, review) VALUES ("
            << user_id << ", "
            << book_id << ", "
            << rating << ", '"
            << review << "');";

        char* errMsg = nullptr;
        if (sqlite3_exec(db, sql.str().c_str(), callback, nullptr, &errMsg) != SQLITE_OK) {
            cerr << "SQL error: " << errMsg << endl;
            sqlite3_free(errMsg);
        } else {
            cout << "Rating added successfully\n";
        }
    }
};

int main() {
    DatabaseManager db("library.db");

    // Create tables in the database
    db.createTables();

    // Add some records
    db.addUser("johndoe", "hashed_password", "johndoe@example.com", "librarian");
    db.addAuthor("J.K. Rowling", "1965-07-31", "British author, best known for the Harry Potter series.");
    db.addBook("Harry Potter and the Philosopher's Stone", 1, "1997-06-26", "9780747532699", 10);
    db.addCategory("Fantasy", "Books that involve magic and fantastical elements.");
    db.addRating(1, 1, 5, "An amazing book!");
    db.addBorrowing(1, 1, "2025-02-28");

    return 0;
}
