# __init__.py
from flask import Flask
from dotenv import load_dotenv
from .routes.admin import admin
from .routes.views import views
from .routes.documents import document_handler
from .extensions import db, migrate
from datetime import datetime
import humanize
import os

load_dotenv()


def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/dbpweb'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.jinja_env.globals.update(zip=zip)
    app.jinja_env.globals.update(datetime=datetime)
    app.jinja_env.filters['humanize'] = humanize.naturaltime

    db.init_app(app=app)
    migrate.init_app(app=app, db=db)

    # Blueprint registration
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(admin, url_prefix='/admin')
    app.register_blueprint(document_handler, url_prefix='/documents')

    return app
