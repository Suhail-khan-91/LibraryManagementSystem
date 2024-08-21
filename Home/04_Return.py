import streamlit as st
import sqlite3
from datetime import datetime


# Connect to SQLite database
def get_db_connection():
    conn = sqlite3.connect('library.db')
    return conn


def show_page():
    if st.session_state.role == 'student':
        st.title("Book Return 🔄")

        # Connect to the database
        conn = get_db_connection()
        cursor = conn.cursor()

        # Fetch books the student currently has checked out
        student_id = st.session_state.student_id
        cursor.execute('''
            SELECT books.book_id, books.book_name
            FROM requests
            JOIN books ON requests.book_id = books.book_id
            WHERE requests.student_id = ? AND requests.status = 'Approved'
        ''', (student_id,))
        checked_out_books = cursor.fetchall()

        if checked_out_books:
            book_ids, book_names = zip(*checked_out_books)
            selected_book_name = st.selectbox("Select Book to Return:", book_names)

            if st.button("Return Book"):
                # Find the selected book_id
                selected_book_id = book_ids[book_names.index(selected_book_name)]

                try:
                    # Insert return request into the return_requests table
                    request_date = datetime.now().strftime('%Y-%m-%d')
                    cursor.execute(
                        "INSERT INTO return_requests (student_id, book_id, request_date, status) VALUES (?, ?, ?, ?)",
                        (student_id, selected_book_id, request_date, 'Pending'))
                    conn.commit()

                    st.write(f"Return request for book '{selected_book_name}' submitted successfully!")
                except Exception as e:
                    st.write(f"An error occurred: {e}")

            conn.close()
        else:
            st.write("You have no books checked out.")
    else:
        st.write("Access denied. Please log in to access this page.")


if 'role' in st.session_state and st.session_state.role == 'student':
    show_page()
else:
    st.write("Please log in to access this page.")
