import re
import uuid
from flask import Blueprint, flash, redirect, request, render_template, session, jsonify
from flask.ext.login import login_required
from areas.wanted.models.book import BookWanted
from areas.wanted.models.forms import NewBookWantedForm
from areas.user.models.user import User
import infrastructure

__author__ = 'teopost'


wanted_app = Blueprint('wanted', __name__, static_folder='static', template_folder='templates')

login_manager = infrastructure.login_manager
admin = infrastructure.admin
db = infrastructure.db


@wanted_app.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    form = NewBookWantedForm()
    form.owner = session.get('user_id', None)

    if request.method == 'GET':
        return render_template('wanted/new.html', form=form)
    try:
        if form.validate_on_submit():
            flash('Success')
            book = BookWanted()
            form.populate_obj(book)
            book.id = str(uuid.uuid4())  # workaround: duplication errors during item creation
            book.owner = session.get('user_id', None)
            book.save()

            return redirect('/wanted/my')
    except Exception, e:
        print str(e)

    return render_template('wanted/new.html', form=form)


@wanted_app.route('/my')
@wanted_app.route('/my/<page_id>')
def my_books_list(page_id=1):
    user_id = session.get('user_id', None)
    if user_id:

        paginated_books = BookWanted.objects(owner=user_id).paginate(page=page_id, per_page=15)
        return render_template('wanted/my_list.html', books=paginated_books, user=session.get('user_name'))

    return redirect('user/login')


@wanted_app.route('/details/<book_id>')
def book_details(book_id):
    book = BookWanted.objects(id=book_id).first()
    if book:
        is_owner = book.owner == session.get('user_id', None)
        owner_details = User.objects(id=str(book.owner)).first()
        return render_template('wanted/details.html', book=book, owner=owner_details, is_owner=is_owner)

    return redirect('/wanted/my')

@wanted_app.route('/search')
def search():
    return render_template('wanted/search.html')


