from hashlib import sha256

from .database import engine, Base, LocalSession
from .models import User


def add_user():

    email = "samisamiyev@gmail.com"
    password = "1234"
    first_name = "sami"
    last_name = "samiyev"

    db = LocalSession()
    
    user = db.query(User).filter(User.email == email).first()
    if user:
        print("user mavjud")
        return
   
    hashed_password = sha256(password.encode()).hexdigest()
    new_user = User(
        first_name=first_name,
        last_name=last_name,
        email=email,
        hashed_password=hashed_password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

def get_users():
    db = LocalSession()

    users = db.query(User).all()
    print(users)

def update_user():
    db = LocalSession()

    user = db.query(User).filter_by(email = "alivaliyev@gmail.com").first()
    user.first_name = "Updated Ali"

    db.commit()

def delete_user():
    db = LocalSession()

    user = db.query(User).filter_by(email = "alivaliyev@gmail.com").first()
    
    db.delete(user)

    db.commit()

def login():
    email = "valialiyev@gmail.com"
    password = "1234"

    hashed_password = sha256(password.encode()).hexdigest()

    db = LocalSession()

    user = db.query(User).filter(
        User.email == email, 
        User.hashed_password == hashed_password).first()
    if user:
        print("siz login qilindingiz")
        return
    
    print("user topilmadi")


def main():

    # add_user()
    # update_user()
    # delete_user()
    # get_users()
    login()

    
    Base.metadata.create_all(engine)

