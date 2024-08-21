import sqlite3
import streamlit as st
import pandas as pd


def get_db_connection():
    conn = sqlite3.connect('library.db')
    return conn


def show_page():
    if st.session_state.role == 'librarian':
        st.title("All Transaction History 🗂️")

        conn = get_db_connection()
        cursor = conn.cursor()

        print("Fetching checkout history...")
        cursor.execute("SELECT * FROM requests")
        checkout_history = cursor.fetchall()

        print("Fetching return history...")
        cursor.execute("SELECT * FROM return_requests")
        return_history = cursor.fetchall()

        st.subheader("Checkout History")
        if checkout_history:
            checkout_df = pd.DataFrame(checkout_history,
                                       columns=['request_id', 'student_id', 'book_id', 'request_date', 'status'])
            st.write("Checkout Requests:")
            st.table(checkout_df)
        else:
            st.write("No checkout history found.")

        st.subheader("Return History")
        if return_history:
            return_df = pd.DataFrame(return_history,
                                     columns=['return_request_id', 'student_id', 'book_id', 'request_date', 'status'])
            st.write("Return Requests:")
            st.table(return_df)
        else:
            st.write("No return history found.")

        conn.close()
    else:
        st.write("Access denied. Please log in as a librarian.")
