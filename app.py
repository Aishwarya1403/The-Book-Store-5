import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from models import setup_db, Books, Categories
from auth import AuthError, requires_auth


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    CORS(app)
    setup_db(app)

    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PATCH,POST,DELETE,OPTIONS')
        return response

    @app.route('/')  # gives all the books
    def all_books():
        all_books = Books.query.all()
        formatted = [book.format() for book in all_books]
        return jsonify({
            "success": True,
            "books": formatted
        }), 200

    @app.route('/books')  # gives all the books
    @requires_auth('get:books')
    def all_books(payload):
        all_books = Books.query.all()
        formatted = [book.format() for book in all_books]
        return jsonify({
            "success": True,
            "books": formatted
        }), 200

    @app.route('/categories/<int:id>')  # id represents the id of the books
    @requires_auth('get:books_by_id')
    def books_by_category(payload, id):
        try:
            books = Books.query.filter(Books.id == id).one_or_none()
            if id is None:
                abort(422)
            else:
                return jsonify({
                    "success": True,
                    "by_id": books.format()
                }), 200
        except Exception:
            abort(404)

    # id here is the group id in which book is to be added
    @app.route('/categories/<int:id>', methods=['POST'])
    @requires_auth('post:books')
    def new_books(payload, id):
        try:
            data = request.get_json()
            add_name = data.get('name')
            add_author = data.get('author')
            add_category = data.get('category_id')
            new_addition = Books(
                name=add_name, author=add_author, category_id=add_category)
            new_addition.insert()

            return jsonify({
                "name": add_name,
                "author": add_author,
                "category": add_category,
                "success": True,
                "message": "successfully added a new book"
            }), 200
        except Exception:
            abort(422)

    # id is the unique id of the book
    @app.route('/categories/<int:id>', methods=['DELETE'])
    @requires_auth('delete:books')
    def delete_book(payload, id):
        try:
            book = Books.query.filter(Books.id == id).one_or_none()
            if book is None:
                abort(404)
            else:
                book.delete()
                return jsonify({
                    "success": True,
                    "message": "Book has been deleted",
                    "id": id
                }), 200

        except Exception:
            abort(403)

    # id is the unique id of the book
    @app.route('/category/<int:id>', methods=['PATCH'])
    @requires_auth('patch:books')
    def change(payload, id):
        try:
            data = request.get_json()
            to_change = Books.query.filter(Books.id == id).one_or_none()
            if id is None:
                abort(500)
            else:
                to_change.name = data.get('name')
                to_change.author = data.get('author')
                to_change.category_id = data.get('category_id')

                changed = to_change.update()
                return jsonify({
                    "success": True,
                    "message": "successfully updated the book",
                    "update": changed
                }), 200
        except Exception:
            abort(404)

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "Unprocessable Entity"
        }), 422

    @app.errorhandler(403)
    def bad_req(error):
        return jsonify({
            "success": False,
            "error": 403,
            "message": "Forbidden/Unauthorized"
        }), 403

    @app.errorhandler(404)
    def bad_req(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Not Found"
        }), 404

    @app.errorhandler(500)
    def internal_server(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "Internal Server Error"
        })

    @app.errorhandler(AuthError)
    def handle_autherror(exception):
        res = jsonify(exception.error)
        res.status_code = exception.status_code
        return res

    return app


app = create_app()


if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)
