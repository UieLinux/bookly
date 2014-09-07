import datetime
from areas.catalog.models.book import Book
import infrastructure
from flask import Blueprint, session, request, redirect
from areas.user.models.private_message import PrivateMessage


__author__ = 'carlozamagni'


private_messaging_app = Blueprint('messaging', __name__, static_folder='static', template_folder='templates')

login_manager = infrastructure.login_manager
admin = infrastructure.admin
db = infrastructure.db

@private_messaging_app.route('/create', methods=['POST'])
def send_private_message():
    current_user = session.get('user_id', None)
    current_book = request.form['book_id']
    message_body = request.form['message_body']

    if current_user and message_body:

        book = Book.objects(id=current_book).first()

        private_message = PrivateMessage()
        private_message.created_at = datetime.datetime.utcnow()
        private_message.content = message_body
        private_message.from_user = current_user
        private_message.to_user = book.owner
        private_message.related_to_book_id = current_book

    return redirect('/catalog/details/%s' % current_book)