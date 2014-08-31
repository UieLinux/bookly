import uuid
import datetime
from flask import Blueprint, flash, redirect, request, render_template, session, jsonify
from flask.ext.login import login_required
from areas.catalog.models.book import Book
from areas.catalog.models.message import Message
from areas.user.models.user import User
import infrastructure

__author__ = 'carlozamagni'


book_app = Blueprint('book', __name__, static_folder='static', template_folder='templates')

login_manager = infrastructure.login_manager
admin = infrastructure.admin
db = infrastructure.db


@book_app.route('/<book_id>/comments/add', methods=['POST'])
@login_required
def add_comment(book_id):
    current_user = session.get('user_id', None)
    current_user_name = session.get('user_name', None)
    body = request.form['message_body']

    if not current_user or not body or not current_user_name:
        return redirect('/catalog/details/%s' % book_id)

    try:
        new_message = Message()
        new_message.body = body
        new_message.author = current_user
        new_message.author_user_name = current_user_name
        new_message.created_at = datetime.datetime.utcnow()
        new_message.disabled = False

        book = Book.objects(id=book_id).first()
        book.message_thread.append(new_message)
        book.save()

    except Exception, e:
        print str(e)
        # should set-up mongodb logging handler

    return redirect('/catalog/details/%s' % book_id)