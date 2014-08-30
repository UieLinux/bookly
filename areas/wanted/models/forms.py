from flask_wtf import Form
from wtforms import HiddenField, RadioField, StringField
from wtforms.validators import DataRequired
#from isbn import valid_isbn


__author__ = 'teopost'


class NewBookWantedForm(Form):
    #isbn = StringField('isbn', validators=[DataRequired(), valid_isbn], description={'placeholder': 'isbn'})
    isbn = StringField('isbn', validators=[DataRequired()], description={'placeholder': 'isbn'})
    title = StringField('title', validators=[DataRequired()], description={'placeholder': 'titolo'})
    notes = StringField('notes', description={'placeholder': 'note aggiuntive'})

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
