import os

SECRET_KEY = "-\x85\x99Q5\x89\xe7@\x06\xd3\xa6=G\xcf k\xce6'\x16\xd6\xbb\xe6q"
DEBUG = True
DB_USERNAME = 'blarneyosullivan'
DB_PASSWORD = ''
BLOG_DATABASENAME = 'blog'
DB_HOST = os.getenv('IP','0.0.0.0')
DB_URI = "mysql+pymysql://%s:%s@%s/%s" % (DB_USERNAME, DB_PASSWORD, DB_HOST, BLOG_DATABASENAME)
SQLALCHEMY_DATABASE_URI = DB_URI
SQLALCHEMY_TRACK_MODIFICATIONS = True
