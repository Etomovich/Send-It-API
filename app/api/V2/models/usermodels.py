"""Contain User model."""
import psycopg2
from flask import app
from app.db_config import init_db


connection = init_db()
cursor_object = connection.cursor()

class User:
    """Class for user object."""

    def __init__(self, user_id=None, role=None, username=None, email=None, phone =None, password=None):
        """Initialize User class."""
        self.username = username
        self.email = email
        self.password = password
        self.user_id = user_id
        self.role = role
        self.phone = phone

    def serialize_user(self):
        """Return tuple as user dictionary."""
        return dict(
            id=self.user_id,
            username=self.username,
            email=self.email,
            role=self.role,
            phone=self.phone
        )

    @classmethod
    def get_user_by_username(cls, username):
        """Find a user by username."""
        query_user = """SELECT * FROM users WHERE username= %s"""
        cursor_object.execute(query_user, (username,))
        row = cursor_object.fetchone()
        if row:
            user = cls(*row)
        else:
            user = None
        return user

    @classmethod
    def get_user_by_id(cls, _id):
        """Find a user by id."""
        query1 = "SELECT * FROM users WHERE userid= %s"
        cursor_object.execute(query1, (_id,))
        row = cursor_object.fetchone()
        if row:
            user = cls(*row)
        else:
            user = None

        return user
    
    @classmethod
    def insert_into_db(self, user):
        """Method to insert user to database."""
        query1 = """INSERT INTO users (username, email, password) VALUES (%s,%s,%s)""" 
        cursor_object.execute(query1, (user.username,user.email,user.password,) )
        connection.commit()
        

    def get_all_users(self):
        current_users = []
        query = "SELECT * FROM users"
        cursor_object.execute(query)
        rows = cursor_object.fetchall()
        if len(rows)==0:
            return{"message":"no user found"}, 404
        for row in rows:
            user = User(*row)
            current_users.append(user)
        return current_users

class RevokedTokenModel():
  
    """Model revoked token."""
    def __init__(self, token_id=None, jti=None):
        """Initialize this class."""
        self.token_id = token_id
        self.jti = jti

    def add_to_blacklist(self,jti):
        """Add revoked token to db."""
        query = """INSERT INTO revokedtokens (jti) values (%s)"""
        cursor_object.execute(query, (jti,))
        connection.commit()

    def check_token_if_blacklisted(self,jti):
        """Check token if in blacklist."""
        query = """SELECT * FROM revokedtokens WHERE jti = %s"""
        cursor_object.execute(query, (jti,))
        row = cursor_object.fetchone()
        if row:
            return True
        else:
            return False






        