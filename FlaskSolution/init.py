from flask_sqlalchemy import SQLAlchemy
from config import create_app


flask_app = create_app()
celery_app = flask_app.extensions["celery"]
db = SQLAlchemy(flask_app)