import sqlite3
import streamlit as st
import pandas as pd


def get_db_connection():
    conn = sqlite3.connect('library.db')
    return conn


def show_page():
    if st.session_state.role == 'librarian':
        st.title("Checkout Requests 📥")

        conn = get_db_connection()
        cursor = conn.cursor()

        # Fetch pending checkout requests
        cursor.execute("SELECT * FROM requests WHERE status = 'Pending'")
        requests = cursor.fetchall()

        if requests:
            # Column names: request_id, student_id, book_id, request_date, status
            df = pd.DataFrame(requests, columns=['request_id', 'student_id', 'book_id', 'request_date', 'status'])
            st.write("Pending Checkout Requests:")
            st.table(df)

            # Approve or Reject request
            request_id = st.text_input("Enter Request ID to Approve/Reject:", key="checkout_request_id")
            if st.button("Approve Request"):
                if request_id:
                    try:
                        request_id = int(request_id)
                        conn.execute("UPDATE requests SET status = 'Approved' WHERE request_id = ?", (request_id,))
                        conn.execute("UPDATE books SET available = 'No' WHERE book_id = (SELECT book_id FROM requests WHERE request_id = ?)", (request_id,))
                        conn.commit()
                        st.write(f"Request {request_id} approved!")
                    except ValueError:
                        st.write("Invalid Request ID. Please enter a numeric value.")
            if st.button("Reject Request"):
                if request_id:
                    try:
                        request_id = int(request_id)
                        conn.execute("UPDATE requests SET status = 'Rejected' WHERE request_id = ?", (request_id,))
                        conn.commit()
                        st.write(f"Request {request_id} rejected!")
                    except ValueError:
                        st.write("Invalid Request ID. Please enter a numeric value.")
        else:
            st.write("No pending checkout requests.")

        conn.close()
    else:
        st.write("Access denied. Please log in as a librarian.")


if 'role' in st.session_state and st.session_state.role == 'librarian':
    show_page()
else:
    st.write("Please log in to access this page.")
