import sys
from getpass import getpass
from pprint import pprint

from pydantic import ValidationError
from passlib.context import CryptContext

from .database import engine, Base, LocalSession
from .models import User, Task
from .schemas import UserRegister, UserLogin, TaskCreation

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

            return user

    except ValidationError as e:
        pprint(e.errors())

def show_tasks(user):
    db = LocalSession()

    tasks = db.query(Task).filter_by(user_id=user.user_id).all()

    if tasks:
        print(tasks)
    else:
        print("task yoq")

def add_task(user):
    name = input("Name: ")
    description = input("Description: ")

    try:
        task_data = TaskCreation(name=name, description=description)

        db = LocalSession()
        task = Task(name=task_data.name, description=task_data.description, user_id=user.user_id)
        db.add(task)
        db.commit()
        print('task qoshildi')

    except ValidationError as e:
        pprint(e.errors())

def main():
    user = None

    while True:

        if user:
            print("---Menu---")
            print("1. My Tasks")
            print("2. Add Task")
            print("0. Log Out")

            choice = input("> ")
            if choice == '1':
                show_tasks(user)
            elif choice == '2':
                add_task(user)
            elif choice == '0':
                user = None
            else:
                print("bunday menu mavjud emas.")

        else:
            print("---Menu---")
            print("1. Register")
            print("2. Login")
            print("0. Exit")

            choice = input("> ")
            if choice == '1':
                register()
            elif choice == '2':
                user = login()
            elif choice == '0':
                sys.exit()
            else:
                print("bunday menu mavjud emas.")

