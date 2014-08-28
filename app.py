from flask import Flask, render_template, session
from flask.ext.mongoengine import MongoEngine
from flask.ext.login import LoginManager
from flask.ext.admin import Admin
import infrastructure
import sys


app = Flask(__name__)

app.config['SECRET_KEY'] = '123456790'

# db config
app.config['MONGODB_SETTINGS'] = {'DB': 'testing', 'HOST': 'mongodb://bookly:bookly@ds059509.mongolab.com:59509/bookly'}
#app.config['MONGODB_SETTINGS'] = {'DB': 'testing', 'HOST': 'mongodb://localhost:27017/bookly'}
db = MongoEngine()
db.init_app(app)

admin = Admin(app)

# login init
lm = LoginManager()
lm.init_app(app)
lm.login_view = '/user/login'

setattr(sys.modules['infrastructure'], 'login_manager', lm)
setattr(sys.modules['infrastructure'], 'admin', admin)
setattr(sys.modules['infrastructure'], 'db', db)

from areas.user.auth import user_app
app.register_blueprint(blueprint=user_app, url_prefix='/user')

from areas.catalog.catalog import catalog_app
app.register_blueprint(blueprint=catalog_app, url_prefix='/catalog')

from areas.api.search import api
app.register_blueprint(blueprint=api, url_prefix='/api')

@app.route('/')
def home():
    return render_template('home.html')

@app.route("/favicon.ico")
def favicon():
    return app.send_static_file("favicon.ico")


if __name__ == '__main__':
    app.run()
