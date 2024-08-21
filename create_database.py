import sqlite3
import pandas as pd

# Connect to the SQLite database
connection = sqlite3.connect('library.db')
cursor = connection.cursor()

# Create the students table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS students (
        student_id INTEGER PRIMARY KEY,
        student_name TEXT NOT NULL,
        roll_no TEXT NOT NULL
    )
''')

# Create the books table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS books (
        book_id INTEGER PRIMARY KEY,
        book_name TEXT NOT NULL,
        available TEXT NOT NULL
    )
''')

# Create the requests table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS requests (
        request_id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER,
        book_id INTEGER,
        request_date TEXT,
        status TEXT,
        FOREIGN KEY(student_id) REFERENCES students(student_id),
        FOREIGN KEY(book_id) REFERENCES books(book_id)
    )
''')

# Create the return_requests table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS return_requests (
        return_request_id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER,
        book_id INTEGER,
        request_date TEXT,
        status TEXT,
        FOREIGN KEY(student_id) REFERENCES students(student_id),
        FOREIGN KEY(book_id) REFERENCES books(book_id)
    )
''')

# Create the librarians table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS librarians (
        librarian_code TEXT PRIMARY KEY
    )
''')

# Read student data from the Excel file
student_excel_file = 'Home/student_data.xlsx'
df_students = pd.read_excel(student_excel_file)

# Insert student data into the students table
for _, row in df_students.iterrows():
    cursor.execute('''
        INSERT OR IGNORE INTO students (student_id, student_name, roll_no)
        VALUES (?, ?, ?)
    ''', (row['student_id'], row['student_name'], row['roll_no']))

# Read book data from the Excel file
book_excel_file = 'Home/book_data.xlsx'
df_books = pd.read_excel(book_excel_file)

# Convert "Yes"/"No" to the corresponding boolean values
df_books['available'] = df_books['available'].map({'Yes': True, 'No': False})

# Insert book data into the books table
for _, row in df_books.iterrows():
    cursor.execute('''
        INSERT OR IGNORE INTO books (book_id, book_name, available)
        VALUES (?, ?, ?)
    ''', (row['book_id'], row['book_name'], 'Yes' if row['available'] else 'No'))

# Insert a default librarian code (if needed)
cursor.execute('''
    INSERT OR IGNORE INTO librarians (librarian_code)
    VALUES (?)
''', ('lib123',))

# Commit the changes and close the connection
connection.commit()
connection.close()

print("Database created and populated with student and book data successfully.")
