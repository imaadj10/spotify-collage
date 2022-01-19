import os
from flask import Flask
from flask_session import Session

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(64)
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_FILE_DIR'] = './.flask_session/'
Session(app)
app.jinja_env.filters['zip'] = zip

from spotify_collage import routes