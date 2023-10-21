# Capstone Project V

# Import the sqlite module
import sqlite3 as sql

# Connect to the database and get a cursor object
db = sql.connect("ebookstore.db")
cursor = db.cursor()

# Print a confirmation message for sanity check
print("Connection established!")

# Execute cursor to create a table and commit it
cursor.execute("""
    CREATE TABLE IF NOT EXISTS Books(Id INT PRIMARY KEY, 
                                    Title TEXT, 
                                    Author TEXT, 
                                    Qty INT)
    """)
print("Table created!")
db.commit()


# Now we are going to define different functions to carry out different functionalities of the database

# Define a function to add books
def insert_book():
    book_id = int(input("Please enter an ID of the book: "))
    book_title = input("Please enter the title of the book: ")
    book_author = input("Please enter the name/s of author of the book: ")
    book_qty = input("Please enter the number of the books you want to insert: ")

    # Execute cursor insert book into database
    cursor.execute("""
        INSERT INTO Books VALUES(?, ?, ?, ?)
        """, (book_id, book_title, book_author, book_qty))
    print("The book/s has been added!")
    db.commit()


# Define a function to Update book information
def update_books():
    # Call the search_books function to find and display the book user wants to update information
    search_books()

    # Ask user to enter book id and check if that exists in our database
    # Also, use try/ except method to handle the error which can occur due to unexpected user input
    while True:
        try:
            book_id = int(input("Please enter an ID of the book which you want to update: "))
            cursor.execute("""
                SELECT * FROM Books
                WHERE Id = ?""", (book_id,))

            if cursor.fetchone():
                break
            else:
                print("The Book ID you've entered is not valid. Please try again!")
        except ValueError:
            print("Invalid Input. Please try again!")

    # Ask the user what they want to update or change
    update_info = input("What do you want to update/change(Author or Qty): ").lower()

    # Using if statements to check what a user wants to update and execute it accordingly
    if update_info == "author":
        book_author = input("Please enter the updated name/s of author of the book: ")
        cursor.execute("""
                UPDATE Books SET Author = ? WHERE Id = ?
                """, (book_author, book_id))
    elif update_info == "qty":
        book_qty = int(input("Please enter the updated number of the books you want to insert: "))
        cursor.execute("""
                UPDATE Books SET Qty = ? WHERE Id = ?
                """, (book_qty, book_id))
    else:
        print("Invalid Input. Please try again!")

    print("The book detail/s has been update!")
    db.commit()


# Define a function to delete book
def delete_book():
    # Call the search_books function to find and display the book user wants to delete
    search_books()

    # Ask the user to enter the ID of the book to be deleted
    book_id = int(input("Please enter an ID of the book which you want to delete: "))

    # Execute cursor to delete book
    cursor.execute("""
        DELETE FROM Books WHERE Id=?
        """, (book_id,))
    db.commit()
    print(f"The book with ID {book_id} has been deleted!")


# Define a function to search books
def search_books():
    search_by = input("Please enter anything that matches the book's Title/Author/Id: ")
    # Check if the input is an integer, or say an ID and execute cursor accordingly
    if search_by.isdigit():
        cursor.execute("""
            SELECT * FROM Books WHERE Id = ?
            """, (search_by,))
    else:
        # Use % wildcards to match the string and create separate variable to store this
        search_by_str = f"%{search_by}%"
        cursor.execute(f"""
            SELECT * FROM Books WHERE Title LIKE ? OR Author LIKE ?
            """, (search_by_str, search_by_str))

    # Using fetchall function to show the result
    books = cursor.fetchall()
    if books:
        for book in books:
            print(book)
    else:
        print("Could not find a book you're looking for!")


while True:
    # Present the menu to the user
    menu = input(f"""
            \nSelect one of the following options below:
            1 - Add a new book
            2 - Update book information
            3 - Delete a book
            4 - Search for the books
            0 - Exit the system
            : """).lower()

    if menu == "1":
        insert_book()

    elif menu == "2":
        update_books()

    elif menu == "3":
        delete_book()

    elif menu == "4":
        search_books()

    elif menu == "0":
        print("Goodbye!")
        exit()
    else:
        print("Error! You've made a wrong choice. Please try again.")





