import streamlit as st
import sqlite3


# Connect to SQLite database
def get_db_connection():
    conn = sqlite3.connect('library.db')
    return conn


def show_page():
    if st.session_state.role == 'librarian':
        st.title("Return Requests 📥")

        # Connect to the database
        conn = get_db_connection()
        cursor = conn.cursor()

        # Fetch pending return requests
        cursor.execute("SELECT * FROM return_requests WHERE status = 'Pending'")
        return_requests = cursor.fetchall()

        if return_requests:
            st.write("Pending Return Requests")
            for request in return_requests:
                # Ensure the correct number of columns is unpacked
                try:
                    return_request_id, student_id, book_id, request_date, status = request

                    book_cursor = conn.cursor()
                    book_cursor.execute("SELECT book_name FROM books WHERE book_id = ?", (book_id,))
                    book_name = book_cursor.fetchone()[0]

                    col1, col2, col3 = st.columns([3, 1, 1])
                    with col1:
                        st.write(f"Student ID: {student_id}")
                        st.write(f"Book: {book_name}")
                        st.write(f"Request Date: {request_date}")
                    with col2:
                        if st.button(f"Approve {book_id}"):
                            try:
                                # Update request status to 'Approved'
                                cursor.execute("UPDATE return_requests SET status = 'Approved' WHERE return_request_id = ?",
                                               (return_request_id,))
                                # Update book availability
                                cursor.execute("UPDATE books SET available = 'Yes' WHERE book_id = ?", (book_id,))
                                conn.commit()
                                st.write(f"Return request for book '{book_name}' approved.")
                            except Exception as e:
                                st.write(f"An error occurred: {e}")

                    with col3:
                        if st.button(f"Reject {book_id}"):
                            try:
                                # Update request status to 'Rejected'
                                cursor.execute("UPDATE return_requests SET status = 'Rejected' WHERE return_request_id = ?",
                                               (return_request_id,))
                                conn.commit()
                                st.write(f"Return request for book '{book_name}' rejected.")
                            except Exception as e:
                                st.write(f"An error occurred: {e}")

                except ValueError as e:
                    st.write(f"An error occurred while unpacking the request: {e}")

            conn.close()
        else:
            st.write("No pending return requests.")

    else:
        st.write("Access denied. Please log in to access this page.")


if 'role' in st.session_state and st.session_state.role == 'librarian':
    show_page()
else:
    st.write("Please log in to access this page.")
