import sys
# for creating the mapper code
from sqlalchemy import Column, ForeignKey, Integer, String

# for configuration and class code
from sqlalchemy.ext.declarative import declarative_base

# for creating foreign key relationship between the tables
from sqlalchemy.orm import relationship

# for configuration
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# create declarative_base instance
Base = declarative_base()


# Create the class Book and extend it from the Base Class.
class Book(Base):
    __tablename__ = 'book'

    id = Column(Integer, primary_key=True)
    title = Column(String(250), nullable=False)
    author = Column(String(250), nullable=False)
    genre = Column(String(250))

    @property
    def serialize(self):
        return dict(title=self.title, author=self.author, genre=self.genre, id=self.id)


# creates a create_engine instance at the bottom of the file
# Turns off the check_same_thread for simplicity
engine = create_engine('sqlite:///books-collection.db', connect_args={'check_same_thread': False})
Base.metadata.create_all(engine)

DBSession = sessionmaker(bind=engine)
session = DBSession()


def get_all_books():
    return session.query(Book).all()


def get_book_by_id(book_id):
    return session.query(Book).filter_by(id=book_id).one()


def create_update_book(book: Book):
    session.add(book)
    session.commit()
