import datetime
import infrastructure
from flask.ext.login import login_required
from areas.catalog.models.book import Book
from flask import Blueprint, session, request, redirect, render_template
from areas.user.models.private_message import PrivateMessage


__author__ = 'carlozamagni'


private_messaging_app = Blueprint('messaging', __name__, static_folder='static', template_folder='templates')

login_manager = infrastructure.login_manager
admin = infrastructure.admin
db = infrastructure.db


@private_messaging_app.route('/<message_id>')
@login_required
def get_message_details(message_id):
    current_user = session.get('user_id', None)
    message_details = PrivateMessage.find(id=message_id).first()

    if not current_user or (current_user != message_details.to_user):
        return redirect('/messaging/list')

    return render_template('user/message_details.html', message=message_details)


@private_messaging_app.route('/list')
@login_required
def get_messages_list():
    current_user = session.get('user_id', None)
    if not current_user:
        return redirect('user/login')

    messages = PrivateMessage.Find(to_user=current_user)
    return render_template('user/message_list', messages=messages)


@private_messaging_app.route('/create', methods=['POST'])
@login_required
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


@private_messaging_app.route('/reply', methods=['POST'])
@login_required
def reply_to_private_message():
    current_user = session.get('user_id', None)
    current_message = request.form['message_id']
    reply_message_body = request.form['message_body']

    if current_user and current_message and reply_message_body:

        original_message = PrivateMessage.find(id=current_message).first()
        original_message.reply(content=reply_message_body)

    # TODO: redirect to message page (not created yet)