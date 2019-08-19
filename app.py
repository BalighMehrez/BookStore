from flask import Flask, render_template, request, redirect, url_for
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Book
from flask import jsonify

app = Flask(__name__)

# Connect to Database and create database session
engine = create_engine('sqlite:///books-collection.db', connect_args={'check_same_thread': False})
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# landing page that will display all the books in our database
# This function operate on the Read operation.
@app.route('/')
@app.route('/books')
def show_books():
    books = session.query(Book).all()
    return render_template("books.html", books=books)


# This will let us Create a new book and save it in our database
@app.route('/books/new/', methods=['GET', 'POST'])
def new_book():
    if request.method == 'POST':
        created_book = Book(title=request.form['name'], author=request.form['author'], genre=request.form['genre'])
        session.add(created_book)
        session.commit()
        return redirect(url_for('show_books'))
    else:
        return render_template('newBook.html')


# This will let us Update our books and save it in our database
@app.route("/books/<int:book_id>/edit/", methods=['GET', 'POST'])
def edit_book(book_id):
    edited_book = session.query(Book).filter_by(id=book_id).one()
    if request.method == 'POST':
        if request.form['name']:
            edited_book.title = request.form['name']
            return redirect(url_for('show_books'))
    else:
        return render_template('editBook.html', book=edited_book)


# This will let us Delete our book
@app.route('/books/<int:book_id>/delete/', methods=['GET', 'POST'])
def delete_book(book_id):
    book_to_delete = session.query(Book).filter_by(id=book_id).one()
    if request.method == 'POST':
        session.delete(book_to_delete)
        session.commit()
        return redirect(url_for('show_books', book_id=book_id))
    else:
        return render_template('deleteBook.html', book=book_to_delete)


"""
api functions
"""


def get_books():
    books = session.query(Book).all()
    return jsonify(books=[b.serialize for b in books])


def get_book(book_id):
    books = session.query(Book).filter_by(id=book_id).one()
    return jsonify(books=books.serialize)


def make_a_new_book(title, author, genre):
    added_book = Book(title=title, author=author, genre=genre)
    session.add(added_book)
    session.commit()
    return jsonify(Book=added_book.serialize)


def update_book(id, title, author, genre):
    updated_book = session.query(Book).filter_by(id=id).one()
    if not title:
        updated_book.title = title
    if not author:
        updated_book.author = author
    if not genre:
        updated_book.genre = genre
    session.add(updated_book)
    session.commit()
    return 'Updated a Book with id %s' % id


def delete_a_book(id):
    book_to_delete = session.query(Book).filter_by(id=id).one()
    session.delete(book_to_delete)
    session.commit()
    return 'Removed Book with id %s' % id


@app.route('/')
@app.route('/booksApi', methods=['GET', 'POST'])
def books_function():
    if request.method == 'GET':
        return get_books()
    elif request.method == 'POST':
        title = request.args.get('title', '')
        author = request.args.get('author', '')
        genre = request.args.get('genre', '')
        return make_a_new_book(title, author, genre)


@app.route('/booksApi/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def book_function_id(id):
    if request.method == 'GET':
        return get_book(id)

    elif request.method == 'PUT':
        title = request.args.get('title', '')
        author = request.args.get('author', '')
        genre = request.args.get('genre', '')
        return update_book(id, title, author, genre)

    elif request.method == 'DELETE':
        return delete_a_book(id)


if __name__ == '__main__':
    app.debug = True
    app.run()
