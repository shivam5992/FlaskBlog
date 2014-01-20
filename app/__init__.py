import os
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask.ext.openid import OpenID
from config import *

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
lm = LoginManager()
lm.init_app(app)
oid = OpenID(app, os.path.join(basedir, 'tmp'))
lm.login_view = 'login'

'''
Creating a log file in tmp folder
'''
if not app.debug:
	import logging
	from logging.handlers import RotatingFileHandler, SMTPHandler
	file_handler = RotatingFileHandler('tmp/FlaskBlog.log', 'a', 1 * 1024 * 1024, 10)
	file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
	app.logger.setLevel(logging.INFO)
	file_handler.setLevel(logging.INFO)
	app.logger.addHandler(file_handler)
	app.logger.info('microblog startup')
	credentials = None
	if MAIL_USERNAME or MAIL_PASSWORD:
		credentials = (MAIL_USERNAME, MAIL_PASSWORD)
	mail_handler = SMTPHandler((MAIL_SERVER, MAIL_PORT), 'no-reply@' + MAIL_SERVER, 'FlaskBlog failure', credentials)
	mail_handler.setLevel(logging.ERROR)
	app.logger.addHandler(mail_handler)

from app import views, models
