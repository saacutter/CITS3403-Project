from app import db, login
from sqlalchemy import Integer, Text
from sqlalchemy.orm import Mapped, mapped_column
from flask_login import UserMixin
from datetime import datetime, timezone

@login.user_loader
def load_user(id):
    return db.session.get(Users, int(id))

class Users(db.Model, UserMixin):
    id:            Mapped[int]      = mapped_column(Integer, primary_key=True)
    username:      Mapped[str]      = mapped_column(Text, unique=True, nullable=False, index=True)
    email:         Mapped[str]      = mapped_column(Text, unique=True, nullable=False, index=True)
    password:      Mapped[str]      = mapped_column(Text, nullable=False, index=True)
    creation_date: Mapped[datetime] = mapped_column(nullable=False, index=True, default=lambda: datetime.now(timezone.utc))
    last_login:    Mapped[datetime] = mapped_column(nullable=False, index=True, default=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f"{self.id} is {self.username} ({self.email}, {self.password}, {self.creation_date}, {self.last_login})"