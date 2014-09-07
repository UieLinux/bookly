from flask import Blueprint
import infrastructure

__author__ = 'carlozamagni'


private_messaging_app = Blueprint('messaging', __name__, static_folder='static', template_folder='templates')

login_manager = infrastructure.login_manager
admin = infrastructure.admin
db = infrastructure.db