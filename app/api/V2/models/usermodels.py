"""COntain User model."""
import psycopg2
from flask import app
from app.db_config import init_db

connection = init_db()
class User:
    """Class for user object."""

    def __init__(self, _id=None, role=None, username=None, email=None, password=None, phone=None):
        """Initialize User class."""
        self.username = username
        self.email = email
        self.password = password
        self.id = _id
        self.role = role
        self.phone = phone

    def serialize_user(self):
        """Return tuple as user dictionary."""
        return dict(
            id=self.id,
            username=self.username,
            email=self.email,
            role=self.role,
            phone=self.phone
        )

    @classmethod
    def get_by_username(cls, username):
        """Find a user by username."""
        cur = connection.cursor()
        query = """SELECT * FROM users WHERE username= %s"""
        cur.execute(query, (username,))
        row = cur.fetchone()
        if row:
            user = cls(*row)
        else:
            user = None
        return user

    @classmethod
    def get_by_id(cls, _id):
        """Find a user by id."""
        cur = connection.cursor()
        query = "SELECT * FROM users WHERE userid= %s"
        cur.execute(query, (_id,))
        row = cur.fetchone()
        if row:
            user = cls(*row)
        else:
            user = None

        return user


   