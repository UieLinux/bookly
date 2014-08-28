import re
from flask import Blueprint, request, jsonify
from areas.catalog.models.book import Book
import infrastructure

__author__ = 'carlozamagni'


api = Blueprint('api', __name__, static_folder='static', template_folder='templates')

login_manager = infrastructure.login_manager
admin = infrastructure.admin
db = infrastructure.db


@api.route('/search')
def search():
    full_text_search_query = request.args.get('q')
    isbn_query = request.args.get('isbn')

    q_result = None
    if isbn_query:
        q_result = Book.objects(isbn=isbn_query)

    if not q_result and full_text_search_query:
        regx = re.compile(full_text_search_query, re.IGNORECASE)
        q_result = Book.objects(__raw__={'$or': [{'title': regx},
                                                 {'author': regx},
                                                 {'notes': regx}]})
    book_results = []
    for b in q_result:
        book_results.append(b.dict_representation())

    return jsonify(book_results)