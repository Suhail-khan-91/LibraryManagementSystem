import sqlite3
import streamlit as st
import pandas as pd


# Remove caching for testing
def fetch_data(student_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Fetch book checkout history
    cursor.execute("SELECT * FROM requests WHERE student_id = ?", (student_id,))
    checkout_history = cursor.fetchall()

    # Fetch book return history
    cursor.execute("SELECT * FROM return_requests WHERE student_id = ?", (student_id,))
    return_history = cursor.fetchall()

    conn.close()

    return checkout_history, return_history


def get_db_connection():
    conn = sqlite3.connect('library.db')
    return conn


def show_page():
    if st.session_state.role == 'student':
        if 'student_id' not in st.session_state:
            st.write("Error: Student ID not found. Please log in again.")
            return

        st.title("Book History 📜")

        student_id = st.session_state.student_id  # Assuming student_id is set in session state

        # Fetch data
        checkout_history, return_history = fetch_data(student_id)

        # Display checkout history
        st.subheader("Checkout History")
        if checkout_history:
            # Column names: request_id, student_id, book_id, request_date, status
            checkout_df = pd.DataFrame(checkout_history,
                                       columns=['Request ID', 'Student ID', 'Book ID', 'Request Date', 'Status'])
            st.write("Checkout Requests:")
            st.table(checkout_df)
        else:
            st.write("No checkout history found.")

        # Display return history
        st.subheader("Return History")
        if return_history:
            # Column names: return_request_id, student_id, book_id, request_date, status
            return_df = pd.DataFrame(return_history,
                                     columns=['Return Request ID', 'Student ID', 'Book ID', 'Request Date', 'Status'])
            st.write("Return Requests:")
            st.table(return_df)
        else:
            st.write("No return history found.")
    else:
        st.write("Access denied. Please log in as a student.")


if 'role' in st.session_state and st.session_state.role == 'student':
    show_page()
else:
    st.write("Please log in to access this page.")
