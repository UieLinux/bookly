import datetime
import infrastructure

__author__ = 'carlozamagni'


db = infrastructure.db


class Message(db.EmbeddedDocument):
    created_at = db.DateTimeField(default=datetime.datetime.now, required=True)
    body = db.StringField(verbose_name="review", required=True)
    author = db.StringField(verbose_name="author_id", max_length=255, required=True)
    author_user_name = db.StringField(verbose_name="author_user_name", max_length=255, required=True)
    disabled = db.BooleanField(default=False)

    def __unicode__(self):
        return '%s - %s' % (self.created_at, self.author)

    def dict_representation(self):

        return {'created_at': self.created_at,
                'author_user_name': self.author_user_name,
                'body': self.body}