from app import db, login
from sqlalchemy import Integer, Text, ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column
from flask_login import UserMixin
from datetime import datetime, timezone, time
import enum


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

class FriendRequestStatus(enum.Enum):
    pending = "pending"
    accepted = "accepted"
    declined = "declined"

class FriendRequest(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    from_user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    to_user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    status: Mapped[FriendRequestStatus] = mapped_column(Enum(FriendRequestStatus), nullable=False, default=FriendRequestStatus.pending)
    timestamp: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    def __repr__(self):
        return f"<FriendRequest from {self.from_user_id} to {self.to_user_id} - {self.status}>"