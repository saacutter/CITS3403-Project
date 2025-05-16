from app import db, login
import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timezone
from typing import List

@login.user_loader
def load_user(id):
    return Users.query.get(id)

class Users(db.Model, UserMixin):
    id:              Mapped[int]      = mapped_column(db.Integer, primary_key=True)
    username:        Mapped[str]      = mapped_column(db.Text, unique=True, nullable=False, index=True)
    email:           Mapped[str]      = mapped_column(db.Text, unique=True, nullable=False, index=True)
    password:        Mapped[str]      = mapped_column(db.String(128), nullable=False, index=True)
    profile_picture: Mapped[str]      = mapped_column(nullable=False, index=True)
    private:         Mapped[bool]     = mapped_column(nullable=False, index=True, default=True)
    creation_date:   Mapped[datetime] = mapped_column(nullable=False, index=True, default=lambda: datetime.now(timezone.utc))
    last_login:      Mapped[datetime] = mapped_column(nullable=False, index=True, default=lambda: datetime.now(timezone.utc))
    tournaments:     Mapped[List["Tournaments"]] = db.relationship('Tournaments', backref='user')
    
    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    def serialise(self):
        return {
            "username": self.username,
            "last_login": self.last_login,
            "profile_picture": self.profile_picture
        }
    
    def is_friends_with(self, user):
        return db.session.scalar(sa.select(Friends).where((Friends.to_user == self.id) & (Friends.from_user == user.id))) is not None

class Friends(db.Model):
    id:        Mapped[int]      = mapped_column(db.Integer, primary_key=True)
    to_user:   Mapped[int]      = mapped_column(db.Integer, db.ForeignKey('users.id'))
    from_user: Mapped[int]      = mapped_column(db.Integer, db.ForeignKey('users.id'))
    added_on:  Mapped[datetime] = mapped_column(nullable=False, default=lambda: datetime.now(timezone.utc))

    def getUser(id):
        return db.session.scalar(sa.select(Users).where((Users.id == id)))
    
class Tournaments(db.Model):
    id:         Mapped[int] = mapped_column(db.Integer, primary_key=True)
    user_id:    Mapped[int] = mapped_column(db.Integer, db.ForeignKey('users.id'))
    name:       Mapped[str] = mapped_column(db.Text, nullable=False, index=True)
    game_title: Mapped[str] = mapped_column(db.Text, nullable=False, index=True)
    date:       Mapped[str] = mapped_column(db.Text, nullable=False, index=True)
    points:     Mapped[int] = mapped_column(db.Integer, nullable=False, index=True, default=0)
    result:     Mapped[str] = mapped_column(db.Text, nullable=False, index=True)
    details:    Mapped[str] = mapped_column(db.Text, nullable=True) 
    image:      Mapped[str] = mapped_column(db.Text, nullable=True)