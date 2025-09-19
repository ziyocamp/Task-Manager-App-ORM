from hashlib import sha256

from .database import engine, Base, LocalSession
from .models import User


def add_user():
    password = "1234"
    hashed_password = sha256(password.encode()).hexdigest()
    new_user = User(
        first_name="ali",
        last_name="valiyev",
        email="alivaliyev@gmail.com",
        hashed_password=hashed_password
    )

    db = LocalSession()
    db.add(new_user)
    db.commit()
    db.refresh(new_user)


def main():

    add_user()
    
    Base.metadata.create_all(engine)

