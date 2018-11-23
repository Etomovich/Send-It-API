"""Contain db connection fuctions."""
import psycopg2
from passlib.hash import sha256_crypt
from app.config import app_config

env = app_config['production']
url = env.url

def connection(url):
    """Connection initiated."""
    conn = psycopg2.connect(url)
    return conn


def init_db():
    """Method start conenction."""
    conn = psycopg2.connect(url)
    return conn

def create_super_admin():
    """Fuction create a super admin."""
    username = "serem"
    phone = 700278037
    password = sha256_crypt.encrypt("andela")
    query = """SELECT * FROM users WHERE username= %s"""
    conn = init_db()
    cur = conn.cursor()
    cur.execute(query, (username,))
    row = cur.fetchone()
    if not row:
        query = "INSERT INTO users (role, username, email, phone, password) VALUES(%s,%s,%s,%s,%s)"
        conn = init_db()
        cur = conn.cursor()
        cur.execute(query,('admin',username,'brian@brian.com',21454585,password))
        conn.commit()
    else:
        conn.close()

def create_super_user():
    """Fuction create a super admin."""
    username = "hulk"
    phone = 700278037
    password = sha256_crypt.encrypt("incredible")
    query = """SELECT * FROM users WHERE username= %s"""
    conn = init_db()
    cur = conn.cursor()
    cur.execute(query, (username,))
    row = cur.fetchone()
    if not row:
        query = "INSERT INTO users (username, email, phone, password) VALUES(%s,%s,%s,%s)"
        conn = init_db()
        cur = conn.cursor()
        cur.execute(query,(username,'brian@brian.com',21454585,password))
        conn.commit()
    else:
        conn.close()

    
    

def create_orders_table():
    """Create orders table."""
    query_tables = """CREATE TABLE IF NOT EXISTS orders(
    order_id SERIAL PRIMARY KEY,
    name CHARACTER VARYING(200) NOT NULL,
    destination CHARACTER VARYING(200) NOT NULL,
    origin CHARACTER VARYING(200) NOT NULL,
    price SERIAL  NOT NULL,
    weight SERIAL  NOT NULL,
    status CHARACTER VARYING(200) DEFAULT 'pending',
    user_id SERIAL,
    curr_location CHARACTER VARYING(200) DEFAULT 'sendithq') ; """
    conn = init_db()
    cur = conn.cursor()
    cur.execute(query_tables)
    conn.commit()
    


def create_users_table():
    """Create users table."""
    query_users = """CREATE TABLE IF NOT EXISTS users(
    userid SERIAL PRIMARY KEY,
    role CHARACTER VARYING(200) DEFAULT 'customer',
    username CHARACTER VARYING(200) NOT NULL,
    email CHARACTER VARYING(200) NOT NULL,
    phone SERIAL,
    password CHARACTER VARYING(200) NOT NULL);"""
    conn = init_db()
    cur = conn.cursor()
    cur.execute(query_users)
    conn.commit()

def destroy_tables():
    """Destroy tables method."""
    conn = init_db()
    cur = conn.cursor()
    orders = "DROP TABLE IF EXISTS orders CASCADE;"
    users = """DROP TABLE IF EXISTS users CASCADE;"""
    tables = [users,orders]
    for table in tables:
        cur.execute(table)
    conn.commit()
