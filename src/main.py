from .database import engine


def main():
    conn = engine.connect()

    conn.close()

