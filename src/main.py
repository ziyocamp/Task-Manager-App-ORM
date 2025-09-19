from .database import engine, Base
from .models import User


def main():
    
    Base.metadata.create_all(engine)

