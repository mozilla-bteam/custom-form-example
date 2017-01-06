from flask import Flask
from routes import route
from models import db
import os

app = Flask(__name__)
app.register_blueprint(route)
db.init_app(app)
app.secret_key = 'a_random_string_which_you_need_to_protect_your_custom_form_during_production'
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
    os.path.dirname(os.path.abspath(__file__)) + '/sqlite3.db'

if __name__ == '__main__':
    app.run()
