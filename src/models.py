from sqlalchemy import (
    Column,
    Integer,
    String,
)
from .database import Base


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True)
    first_name = Column(String(64), nullable=False)
    last_name = Column(String(64))
    email = Column(String(256), unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    @property
    def fullname(self) -> str:
        if self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.first_name

    def __repr__(self) -> str:
        return f"User(id={self.user_id}, name={self.email}, fullname={self.fullname})"
