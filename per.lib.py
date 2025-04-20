import streamlit as st
import json
import os

# --- File Handling ---
FILE_NAME = "library.json"

# Load library from file
def load_library():
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r") as file:
            return json.load(file)
    return []

# Save library to file
def save_library(library):
    with open(FILE_NAME, "w") as file:
        json.dump(library, file, indent=4)

# Initialize session state
if "library" not in st.session_state:
    st.session_state.library = load_library()

# Add a book
def add_book():
    st.markdown("<h2 style='color:#6A5ACD;'>📚 Add a Book</h2>", unsafe_allow_html=True)
    title = st.text_input("📖 Title")
    author = st.text_input("✍️ Author")
    year = st.number_input("📅 Publication Year", min_value=0, step=1)
    genre = st.text_input("🏷️ Genre")
    read_status = st.selectbox("✅ Have you read this book?", ["Yes", "No"])
    link = st.text_input("🔗 Link to the Book (optional)")

    if st.button("➕ Add Book"):
        book = {
            "title": title,
            "author": author,
            "year": int(year),
            "genre": genre,
            "read": read_status == "Yes",
            "link": link
        }
        st.session_state.library.append(book)
        save_library(st.session_state.library)
        st.success("✅ Book added successfully!")

# Remove a book
def remove_book():
    st.markdown("<h2 style='color:#DC143C;'>🗑️ Remove a Book</h2>", unsafe_allow_html=True)
    titles = [book['title'] for book in st.session_state.library]
    if not titles:
        st.info("📭 No books to remove.")
        return
    selected_title = st.selectbox("📘 Select a book to remove", titles)
    if st.button("❌ Remove Book"):
        st.session_state.library = [b for b in st.session_state.library if b['title'] != selected_title]
        save_library(st.session_state.library)
        st.success("🗑️ Book removed successfully!")

# Search for a book
def search_book():
    st.markdown("<h2 style='color:#228B22;'>🔍 Search for a Book</h2>", unsafe_allow_html=True)
    search_by = st.radio("🔎 Search by", ["Title", "Author"])
    query = st.text_input("Enter your search query")

    if query:
        results = []
        for book in st.session_state.library:
            if search_by == "Title" and query.lower() in book["title"].lower():
                results.append(book)
            elif search_by == "Author" and query.lower() in book["author"].lower():
                results.append(book)

        if results:
            st.subheader("📖 Matching Books:")
            for i, b in enumerate(results, 1):
                st.markdown(f"""
                <div style='background-color:#f0f8ff; padding:10px; border-radius:10px; margin-bottom:10px;'>
                    <b>{i}. {b['title']}</b> by <i>{b['author']}</i> ({b['year']})<br>
                    Genre: <b>{b['genre']}</b> | Status: {"✅ Read" if b['read'] else "📖 Unread"}
                    {'<br><a href="' + b['link'] + '" target="_blank">🔗 Link to Book</a>' if b.get('link') else ''}
                </div>
                """, unsafe_allow_html=True)
        else:
            st.warning("🔍 No matching books found.")

# Display all books
def display_books():
    st.markdown("<h2 style='color:#4169E1;'>📚 All Books</h2>", unsafe_allow_html=True)
    if not st.session_state.library:
        st.info("📭 Library is empty.")
    else:
        for i, b in enumerate(st.session_state.library, 1):
            st.markdown(f"""
            <div style='background-color:#e6f7ff; padding:10px; border-radius:10px; margin-bottom:10px;'>
                <b>{i}. {b['title']}</b> by <i>{b['author']}</i> ({b['year']})<br>
                Genre: <b>{b['genre']}</b> | Status: {"✅ Read" if b['read'] else "📖 Unread"}
                {'<br><a href="' + b['link'] + '" target="_blank">🔗 Link to Book</a>' if b.get('link') else ''}
            </div>
            """, unsafe_allow_html=True)

# Show statistics
def show_stats():
    st.markdown("<h2 style='color:#FF8C00;'>📊 Library Statistics</h2>", unsafe_allow_html=True)
    total = len(st.session_state.library)
    read_books = sum(1 for b in st.session_state.library if b["read"])
    percent_read = (read_books / total * 100) if total else 0

    st.markdown(f"""
    <div style='background-color:#fff5e6; padding:10px; border-radius:10px;'>
        <b>Total books:</b> {total}<br>
        <b>Books read:</b> {read_books}<br>
        <b>📈 Percentage read:</b> {percent_read:.2f}%
    </div>
    """, unsafe_allow_html=True)

# Sidebar menu
st.sidebar.markdown("<h1 style='color:#4B0082;'>📖 Library Manager</h1>", unsafe_allow_html=True)
menu = st.sidebar.radio("📋 Choose an action", [
    "Add a Book",
    "Remove a Book",
    "Search for a Book",
    "Display All Books",
    "Display Statistics"
])

# Call appropriate function
if menu == "Add a Book":
    add_book()
elif menu == "Remove a Book":
    remove_book()
elif menu == "Search for a Book":
    search_book()
elif menu == "Display All Books":
    display_books()
elif menu == "Display Statistics":
    show_stats()
