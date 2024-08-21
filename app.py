import streamlit as st
import os
import importlib

# Set the page title and icon
st.set_page_config(page_title="Library Management System", page_icon="📚")


# Sidebar setup
st.sidebar.title("Library Dashboard")

# Ensure the 'Home' directory exists
if not os.path.exists('Home'):
    st.error("The 'Home' directory does not exist.")
else:
    # Define a mapping of filenames to display names and roles
    page_info = {
        '01_Home': ('Home/Login Page', 'common'),
        '02_Book_Search': ('Book Search', 'student'),
        '03_Checkout': ('Book Checkout', 'student'),
        '04_Return': ('Book Return', 'student'),
        '05_Transaction': ('My Transactions History', 'student'),
        '06_Checkout_Requests': ('Checkout Requests', 'librarian'),
        '07_Return_Requests': ('Return Requests', 'librarian'),
        '08_Transaction_History': ('All Transaction History', 'librarian')
    }

    # Initialize selected_page variable
    selected_page = None

    # Display Common Pages
    st.sidebar.markdown("### Login Page")
    common_pages = [display_name for filename, (display_name, role) in page_info.items() if role == 'common']
    selected_common_page = st.sidebar.selectbox("Common Page", common_pages, label_visibility="collapsed")
    for filename, (display_name, role) in page_info.items():
        if display_name == selected_common_page:
            selected_page = filename

    # Display pages for students if the role is 'student'
    if 'role' in st.session_state and st.session_state.role == 'student':
        st.sidebar.markdown("### Student Tools")
        student_pages = [display_name for filename, (display_name, role) in page_info.items() if role == 'student']
        selected_student_page = st.sidebar.selectbox("Choose a page", student_pages)
        for filename, (display_name, role) in page_info.items():
            if display_name == selected_student_page:
                selected_page = filename

    # Display pages for librarians if the role is 'librarian'
    if 'role' in st.session_state and st.session_state.role == 'librarian':
        st.sidebar.markdown("### Librarian Tools")
        librarian_pages = [display_name for filename, (display_name, role) in page_info.items() if role == 'librarian']
        selected_librarian_page = st.sidebar.selectbox("Choose a page", librarian_pages)
        for filename, (display_name, role) in page_info.items():
            if display_name == selected_librarian_page:
                selected_page = filename

    # Dynamically import and show the selected page
    if selected_page:
        try:
            page_module = importlib.import_module(f"Home.{selected_page}")
            if hasattr(page_module, 'show_page'):
                page_module.show_page()
            else:
                st.error(f"Module '{selected_page}' does not have a 'show_page' function.")
        except ModuleNotFoundError as e:
            st.error(f"Error importing module: {e}")
        except Exception as e:
            st.error(f"An error occurred: {e}")
