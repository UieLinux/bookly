from flask_wtf import Form
from wtforms import HiddenField, RadioField, StringField
from wtforms.validators import DataRequired
from isbn import valid_isbn


__author__ = 'carlozamagni'


class NewBookForm(Form):
    isbn = StringField('isbn', validators=[DataRequired(), valid_isbn], description={'placeholder': 'isbn'})
    title = StringField('title', validators=[DataRequired()], description={'placeholder': 'titolo'})
    author = StringField('author', validators=[DataRequired()], description={'placeholder': 'autore'})
    notes = StringField('notes', validators=[DataRequired()], description={'placeholder': 'note aggiuntive'})
    status = RadioField('status', validators=[DataRequired()], choices=[(1, 'abbastanza rovinato'),
                                                                        (2, 'condizioni decenti'),
                                                                        (3, 'accettabile'),
                                                                        (4, 'ben tenuto'),
                                                                        (5, 'come nuovo')], coerce=int)

    owner = HiddenField('owner')

    # see: https://flask-wtf.readthedocs.org/en/latest/form.html
    # recaptcha = RecaptchaField()

    '''
    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
    '''

    def validate(self):
        rv = Form.validate(self)
        if not rv:
            return False

        if not self.status:
            return False

        return True
