import time
import dbLibrary

print("""***********************************
Welcome to the Library Application

Processes:

1. Show books
2. Find  a book
3. Add a book
4. Delete a brook

Enter 'q' for quit.
***********************************""")

lib = dbLibrary.Library()

while True:
    process = input("Process: ")

    if process == "q":
        break
    elif process == "1":
        lib.show_books()

    elif process == "2":
        name = input("Name of the book: ")
        time.sleep(2)
        lib.find_books(name)

    elif process == "3":
        name = input("Name: ")
        author = input("Author: ")
        publisher = input("Publisher: ")
        pages = int(input("Pages: "))

        newBook = dbLibrary.Book(name, author, publisher, pages)
        time.sleep(2)
        lib.add_book(newBook)
        print("New book added successfully")

    elif process == "4":
        name = input("Name of the book: ")
        time.sleep(2)
        lib.delete_book(name)

    else:
        print("Please try again!")
