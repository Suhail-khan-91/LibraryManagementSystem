import sqlite3
import streamlit as st
import pandas as pd
from datetime import datetime


# Function to load available books from the SQLite database
def load_book_data():
    connection = sqlite3.connect('library.db')
    query = "SELECT book_id, book_name FROM books WHERE available = 'Yes'"
    books_df = pd.read_sql(query, connection)
    connection.close()
    return books_df


# Function to request a book checkout
def request_book_checkout(student_id, book_id):
    connection = sqlite3.connect('library.db')
    cursor = connection.cursor()

    # Insert a record into the requests table
    cursor.execute("INSERT INTO requests (student_id, book_id, request_date, status) VALUES (?, ?, ?, ?)",
                   (student_id, book_id, datetime.now().strftime('%Y-%m-%d'), 'Pending'))

    connection.commit()
    connection.close()


def show_page():
    if st.session_state.role == 'student':
        st.title("Book Checkout 📤")

        # Load available books from the database
        books_df = load_book_data()

        # Display available books
        st.subheader("Available Books")
        if not books_df.empty:
            book_options = books_df.set_index('book_id')['book_name'].to_dict()
            selected_book_id = st.selectbox("Select Book to Request:", options=list(book_options.keys()),
                                            format_func=lambda x: book_options[x], key="unique_checkout_selectbox")

            if st.button("Request Book"):
                if selected_book_id:
                    try:
                        # Request book checkout
                        student_id = st.session_state.student_id  # Assuming student_id is set in session state
                        request_book_checkout(student_id, selected_book_id)
                        st.write(f"Request for book '{book_options[selected_book_id]}' submitted successfully!")
                    except Exception as e:
                        st.write(f"An error occurred: {e}")
                else:
                    st.write("Please select a book.")
        else:
            st.write("No books available for checkout.")
    else:
        st.write("Access denied. Please log in as a student.")


if 'role' in st.session_state and st.session_state.role == 'student':
    show_page()
else:
    st.write("Please log in to access this page.")
