from flask import Flask
#from flask.ext.sqlalchemy import SQLALCHEMY
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('settings')
#db = SQLALCHEMY(app)
db = SQLAlchemy(app)

from blog import views
from author import views
