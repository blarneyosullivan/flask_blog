from flask import Flask
#from flask.ext.sqlalchemy import SQLALCHEMY
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.migrate import Migrate
from flaskext.markdown import Markdown

app = Flask(__name__)
app.config.from_object('settings')
#db = SQLALCHEMY(app)
db = SQLAlchemy(app)

# migrations
migrate = Migrate(app, db)

#Markdown
Markdown(app)

from blog import views
from author import views

