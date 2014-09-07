import uuid
import datetime
import infrastructure

__author__ = 'carlozamagni'

db = infrastructure.db


class PrivateMessage(db.Document):
    id = db.StringField(primary_key=True, default=str(uuid.uuid4()))
    related_to_book_id = db.StringField(max_length=200)
    from_user = db.StringField(max_length=200)
    to_user = db.StringField(required=True)
    content = db.StringField(max_length=5000, required=False)

    created_at = db.DateTimeField(required=False, default=datetime.datetime.utcnow())

    def __unicode__(self):
        return 'from: %s to: %s' % (self.from_user, self.to_user)

    def dict_representation(self):
        return {'id': self.id,
                'related_to_book_id': self.related_to_book_id,
                'from_user': self.from_user,
                'to_user': self.to_user,
                'content': self.content,
                'created_at': self.created_at}

