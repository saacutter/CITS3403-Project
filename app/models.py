from app import db

class Users(db.Model):
    id         = db.Column(db.Integer, primary_key=True, nullable=False)
    username   = db.Column(db.Text, nullable=False, unique=True)
    password   = db.Column(db.Text, nullable=False)
    last_login = db.Column(db.DateTime(timezone=False), nullable=False)