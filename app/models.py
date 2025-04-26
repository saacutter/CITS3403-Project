from app import db
from sqlalchemy import Integer, Text
from sqlalchemy.orm import Mapped, mapped_column
from typing import Optional
from datetime import datetime, timezone

class Users(db.Model):
    id:         Mapped[int]      = mapped_column(Integer, primary_key=True)
    username:   Mapped[str]      = mapped_column(Text, unique=True, nullable=False, index=True)
    password:   Mapped[str]      = mapped_column(Text, nullable=False, index=True)
    last_login: Mapped[datetime] = mapped_column(nullable=False, index=True, default=lambda: datetime.now(timezone.utc))

    def __rpr__(self):
        return f"{self.id} {self.username}"