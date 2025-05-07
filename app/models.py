from app import db, login
import sqlalchemy as sa
from sqlalchemy import Integer, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from flask_login import UserMixin
from datetime import datetime, timezone, time

@login.user_loader
def load_user(id):
    return db.session.get(Users, int(id))

class Users(db.Model, UserMixin):
    id:              Mapped[int]      = mapped_column(Integer, primary_key=True)
    username:        Mapped[str]      = mapped_column(Text, unique=True, nullable=False, index=True)
    email:           Mapped[str]      = mapped_column(Text, unique=True, nullable=False, index=True)
    password:        Mapped[str]      = mapped_column(Text, nullable=False, index=True)
    profile_picture: Mapped[str]      = mapped_column(nullable=False, index=True)
    private:         Mapped[bool]     = mapped_column(nullable=False, index=True, default=True)
    creation_date:   Mapped[datetime] = mapped_column(nullable=False, index=True, default=lambda: datetime.now(timezone.utc))
    last_login:      Mapped[datetime] = mapped_column(nullable=False, index=True, default=lambda: datetime.now(timezone.utc))

    def __repr__(self):
         return f"{self.id}, {self.username}, {self.email}, {self.password}, {self.creation_date}, {self.last_login}"
    
    def serialise(self):
        return {
            "username": self.username,
            "last_login": self.last_login,
            "profile_picture": self.profile_picture
        }
    
    def friends_with(self, user):
        # TODO: Return a boolean if the provided user is friends with the user

class Friends(db.Model):
    id:            Mapped[int]      = mapped_column(Integer, primary_key=True)
    user_added:    Mapped[int]      = mapped_column(Integer, db.ForeignKey('users.id'))
    user_added_by: Mapped[int]      = mapped_column(Integer, db.ForeignKey('users.id'))
    added_on:      Mapped[datetime] = mapped_column(nullable=False, default=lambda: datetime.now(timezone.utc))

    def getUser(id):
        db.session.scalar(sa.select(Users).where((Users.username == id)))
    
class Tournaments(db.Model):
    id:         Mapped[int]      = mapped_column(Integer, primary_key=True)
    name:       Mapped[str]      = mapped_column(Text, nullable=False, index=True)
    game_title: Mapped[str]      = mapped_column(Text, nullable=False, index=True)
    date:       Mapped[datetime] = mapped_column(nullable=False, index=True)

    def serialise(self):
        return {
            "name": self.name,
            "game_title": self.game_title,
            "date": self.date
        }

class Matches(db.Model):
    id:         Mapped[int]  = mapped_column(Integer, primary_key=True)
    user_id:    Mapped[int]  = mapped_column(ForeignKey(Users.id, name="matches_user_id"), nullable=False, index=True)
    game:       Mapped[str]  = mapped_column(Text, nullable=False, index=True)
    points:     Mapped[int]  = mapped_column(Integer, nullable=False, index=True, default=0)
    time_taken: Mapped[time] = mapped_column(nullable=False, index=True)
    result:     Mapped[str] = mapped_column(Text, nullable=False, index=True)