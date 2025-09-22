import sys
from hashlib import sha256
from getpass import getpass
from pprint import pprint

from pydantic import ValidationError
from passlib.context import CryptContext

from .database import engine, Base, LocalSession
from .models import User, Task
from .schemas import UserRegister, UserLogin

pwd_context = CryptContext(schemes=["bcrypt"])

Base.metadata.create_all(engine)

def register():
    firstname = input("First Name: ")
    lastname = input("Last Name: ")
    email = input("Email: ")
    password = getpass("Password: ")

    try:
        user_data = UserRegister(first_name=firstname,last_name=lastname,email=email, password=password)

        hashed_password = pwd_context.hash(password)

        db = LocalSession()
        user = User(
            first_name=user_data.first_name, 
            last_name=user_data.last_name,
            email=user_data.email,
            hashed_password=hashed_password
        )
        db.add(user)
        db.commit()
        print('royxatdan otdingiz')

    except ValidationError as e:
        pprint(e.errors())

def login():
    email = input("Email: ")
    password = getpass("Password: ")

    try:
        user_data = UserLogin(email=email, password=password)
        
        db = LocalSession()
        user = db.query(User).filter_by(email=user_data.email).first()

        is_valid = pwd_context.verify(user_data.password, user.hashed_password)
        if is_valid:
            print("login qildingiz")

    except ValidationError as e:
        pprint(e.errors())

def main():
    while True:
        print("---Menu---")
        print("1. Register")
        print("2. Login")
        print("0. Exit")

        choice = input("> ")
        if choice == '1':
            register()
        elif choice == '2':
            login()
        elif choice == '0':
            sys.exit()
        else:
            print("bunday menu mavjud emas.")

