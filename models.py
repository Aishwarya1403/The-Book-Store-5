import os
from sqlalchemy import Column, String, Integer, create_engine, ForeignKey
from flask_sqlalchemy import SQLAlchemy
import json
from sqlalchemy.orm import relationship

database_name = "bookstore"
database_path = "postgres://taofajfsnccdjr:851bab43bc7215395bacf1a183849f5f74d0d48609b77dfb0ec469046c0e345d@ec2-54-210-128-153.compute-1.amazonaws.com:5432/d2p0mft6mv0es2"
db = SQLAlchemy()

def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()


class Books(db.Model):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    author = Column(String)
    category_id = Column(Integer, ForeignKey('category.id'))


    def __init__(self, name, author, category_id):
        self.name = name
        self.author = author
        self.category_id = category_id

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
    def format(self):
        return{
            'id':self.id,
            'name':self.name,
            'author':self.author,
            'category_id':self.category_id
        }


class Categories(db.Model):
    __tablename__= 'category'

    id = Column(Integer, primary_key=True)
    book = relationship("Books", backref="category")
    genre = Column(String)
    language = Column(String)
    

    def __init__(self):
        self.genre = genre

    def format(self):
        return{
            'id':self.id,
            'book':self.book,
            'genre':self.genre,
            'language':self.language
        }

