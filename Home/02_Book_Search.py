import sqlite3
import streamlit as st
import pandas as pd


# Clear session state if not already initialized
if 'initialized' not in st.session_state:
    st.session_state.clear()
    st.session_state.initialized = True


# Function to load book data from the SQLite database
def load_book_data():
    connection = sqlite3.connect('library.db')
    query = "SELECT book_id, book_name, available FROM books"
    df = pd.read_sql(query, connection)
    connection.close()
    return df


# Function to show the Book Search page
def show_page():
    if st.session_state.role == 'student':
        st.title("Book Search 🔎")

        # Load book data from the database
        books_df = load_book_data()

        # Search bar for entering the book name
        search_term = st.text_input("Enter book name:", key="book_search_term_unique_02")

        # Button to trigger the search
        if st.button("Search", key="search_button_unique_02"):
            if search_term:
                connection = sqlite3.connect('library.db')
                query = "SELECT book_id, book_name, available FROM books WHERE book_name LIKE ?"
                filtered_books = pd.read_sql(query, connection, params=('%' + search_term + '%',))
                connection.close()

                # Check if any books were found
                if not filtered_books.empty:
                    st.write("Search Results:")
                    st.dataframe(filtered_books, height=300)  # Display search results as a scrollable table
                else:
                    st.write("No books found.")

        # Display all books in the library
        st.subheader("All Books")
        if not books_df.empty:
            st.dataframe(books_df, height=300)  # Display all books as a scrollable table
        else:
            st.write("No books available.")

    else:
        st.write("Access denied. Please log in as a student.")


# Main logic to show the page if the user is logged in as a student
if 'role' in st.session_state and st.session_state.role == 'student':
    show_page()
else:
    st.write("Please log in to access this page.")
