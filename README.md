APP-URL : https://the-book-store-5.herokuapp.com/

(the JWT for testing are stored in the .env file)

**THE-BOOK-STORE-5**

**Motivation**

This is an online bookstore. It has books of different themes and languages.
(This is just the backend of the app)
 -each book has its unique id.
 -each book is segregated in groups (can be considered as their rating) and can be searched by this by passing as an id.
 -each book has a category_id which depicts its genre and its language.
 -this genre-language set has a unique id. (* this acts as a foreign key while posting new books *)
 -5 operations can be performed on this app ; 
   --get all books
   --get books by their group-id
   --post new books
   --patch existing books
   --delete books by their id.

There are two ROLES for this app namely 'OWNER' and 'KEEPER'. Their roles are defined as follows:

a. Owner:
    The owner can perform all the operations namely
     GET all books
     GET books by group
     POST new books
     PATCH existing books
     DELETE book
    Credentials:    
        id:owner@bookshop.com
        password:Owner100


b. Keeper:
    The keeper can perform the following operations :
     GET all books
     GET books by group
     PATCH existing books
    Credentials:    
        id:keeper@bookshop.com
        password:Keeper22


**Installation**

 #### Python 3.7

To install the latest version of python, follow the link below:
https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python

#### Virtual Enviornment

Virtual environments are a clean way to keep the project dependencies separate from other projects.
To create virtual environment and read more on it, please follow the link below:
https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/


##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py.   
 
- [Heroku](https://devcenter.heroku.com/) is a cloud platform as a service supporting several programming languages.

- [Auth0](https://auth0.com/docs/) is a platform which provides solutions for securing apps.Click on the link to read more.

##### PIP install dependencies 

- Run the following command for the installation of dependencies(recommend to create a virtual environment)
    pip3 install -r requirements.txt

**Database** 
  The database consists of two classes:
    -Books
        books (tablename)
         --this table consists of the * Name of the book, Name of the author, id of the category(id referencing to the theme of the book)
    -Categories
        category (tablename)
         --this table consists of the * Genre of the book and its language *)     
         --this table provides the id for the books table.
         --example of data in this table is as follows:
                id      Genre       Language
                35      Tragic      English

**Endpoints**
    The App consists of the following Endpoints

    **GET('/')**
    
    - doesn't require authentication.
    - returns all the books present in store.
    - request argument : none
    - returns the books in the following format
        "name":"abc",
        "author":"xyz",
        "category_id":37

    **GET('/books')**

    - returns all the books present in store.
    - request argument : none
    - returns the books in the following format
        "name":"abc",
        "author":"xyz",
        "category_id":37

 
    **GET('categories/<int:id>')**

    - returns the book of a certain id. (each book has a group-id)
    - request argument : id
    - example:
        GET('categories/4')
        output:
                {
            "by_id": {
                "author": "Paulo Coehlo",
                "category_id": 37,
                "id": 4,
                "name": "The Alchemist"
                   },
            "success": true 
                }

    **POST('categories/<int:id>')**
    - posts a new book into a new group.
    - request argument : id
    - request body example :
        POST('categories/4')
        {
            "name":"abc",
            "author":"xyz",
            "category_id":35    //this represents the theme related to the book as mentioned in the 'category' table
        }
    - output:
        {
        "author": "xyz",
        "category": 37,
        "message": "successfully added a new book",
        "name": "abc",
        "success": true
        }

    **PATCH('category/<int:id>')**
    - makes changes to the existing books
    - request argument : book_id (the unique book id belonging to each book)
    - request body example :
        PATCH('/category/8')
        {
            "name":"A thousand splendid suns",
            "author":"Khalid Hosseini",
            "category_id":35 
        }    
    

    **DELETE('categories/<int:id>)**
    - deletes the book whose unique id is passed.
    - request argument : book_id (the unique book id belonging to each book)
    - Output for id = 4 (example)
        {  
          "success": True,
          "message": "Book has been deleted",
          "id":4
        }
