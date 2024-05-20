from sqlalchemy import func
from init import db


class CustomerOpinion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now())
    name = db.Column(db.Text)
    text = db.Column(db.Text)
