import pyodbc


class Book:
    def __init__(self, name, author, publisher, pages):
        self.name = name
        self.author = author
        self.publisher = publisher
        self.pages = int(pages)

    def __str__(self):
        return "Name: {}\nAuthor: {}\nPublisher: {}\nPages: {}\n".format(self.name, self.author,
                                                                         self.publisher, self.pages)


class Library:
    def __init__(self):
        self.connect()

    def connect(self):
        self.con = pyodbc.connect("DRIVER={SQL Server};"
                                  "SERVER=localhost;"
                                  "DATABASE=forPython;"
                                  "UID=janfranco;"
                                  "PWD=123456789;"
                                  "Trusted_Connection=yes;")

        self.cursor = self.con.cursor()

        query = "CREATE TABLE books (name varchar(max), author varchar(max), publisher varchar(max), pages int)"

        self.cursor.execute(query)

        self.con.commit()

    def close_connection(self):
        self.con.close()

    def show_books(self):
        query = "SELECT * FROM books"
        self.cursor.execute(query)
        books = self.cursor.fetchall()
        if len(books) == 0:
            print("There is no book!")
        else:
            for i in books:
                print(i)

    def find_books(self, name):

        query = "SELECT * FROM kitaplar WHERE name = ?"
        self.cursor.execute(query, name)
        books = self.cursor.fetchall()

        if len(books) == 0:
            print("Could not found!")
        else:
            for i in books:
                print(i)

    def add_book(self, Book):

        query = "INSERT INTO books ([name], [author], [publisher], [pages]) VALUES (?, ?, ?, ?)"
        self.cursor.execute(query, (Book.name , Book.author, Book.publisher, int(Book.pages)))
        self.con.commit()

    def delete_book(self, name):

        query = "DELETE FROM books WHERE name = ?"
        self.cursor.execute(query, name)
        self.con.commit()
