import streamlit as st
import sqlite3
import time

# Initialize session state if not already initialized
if 'initialized' not in st.session_state:
    st.session_state.clear()
    st.session_state.initialized = True


def authenticate_user(username, password):
    connection = sqlite3.connect('library.db')
    cursor = connection.cursor()
    cursor.execute("SELECT student_id FROM students WHERE student_name = ? AND roll_no = ?", (username, password))
    student = cursor.fetchone()
    cursor.execute("SELECT 1 FROM librarians WHERE librarian_code = ?", (password,))
    librarian = cursor.fetchone()
    connection.close()

    if student:
        return 'student', student[0]
    elif librarian:
        return 'librarian', None
    else:
        return None, None


def show_page():
    st.title("Library Management System 📚")

    user_type = st.radio("Login as:", ["Student", "Librarian"], key="home_user_type_radio")

    if user_type == "Student":
        username = st.text_input("👤 **Enter Username**:", key="home_student_name")
        st.write("(Hint - Username is your first name)")
        password = st.text_input("🔒 **Enter Password**:", type="password", key="home_student_password")
        st.write("(Hint - Password is your roll number)")
    elif user_type == "Librarian":
        username = None
        password = st.text_input("🔑 **Enter Librarian Code**:", type="password", key="home_librarian_password")

    if st.button("Login", key="home_login_button"):
        role, user_id = authenticate_user(username, password) if user_type == "Student" else authenticate_user(None, password)

        if role == 'student':
            st.session_state.role = 'student'
            st.session_state.username = username
            st.session_state.password = password
            st.session_state.student_id = user_id
            st.markdown("**Login successful!**  \n*Please navigate to other pages using the sidebar.*")
            time.sleep(2)  # Delay to show the success message
            st.rerun()
        elif role == 'librarian':
            st.session_state.role = 'librarian'
            st.session_state.username = None
            st.session_state.password = password
            st.session_state.student_id = None
            st.markdown("**Login successful!**  \n*Please navigate to other pages using the sidebar.*")
            time.sleep(2)  # Delay to show the success message
            st.rerun()
        else:
            st.write("Invalid credentials. Please try again.")


if 'role' not in st.session_state:
    show_page()
