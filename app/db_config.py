"""Contain db connection fuctions."""
import psycopg2

url = "dbname=data host=localhost user=brian password= brian"


def connection(url):
    """Connection initiated."""
    conn = psycopg2.connect(url)
    return conn


def init_db():
    """Method start conenction."""
    conn = psycopg2.connect(url)
    return conn


def create_orders_table():
    """Create orders table."""
    query = """CREATE TABLE IF NOT EXISTS orders(
    order_id SERIAL PRIMARY KEY,
    destination CHARACTER VARYING(200) NOT NULL,
    origin CHARACTER VARYING(200) NOT NULL,
    price SERIAL  NOT NULL,
    weight SERIAL  NOT NULL,
    status CHARACTER VARYING(200) DEFAULT 'pending',
    user_id SERIAL  NOT NULL) ; """

    conn = init_db()
    cur = conn.cursor()
    cur.execute(query)
    conn.commit()
    conn.close()


def create_users_table():
    """Create users table."""
    query = """CREATE TABLE IF NOT EXISTS users(
    userid SERIAL PRIMARY KEY,
    role CHARACTER VARYING(200),
    username CHARACTER VARYING(200) NOT NULL,
    email CHARACTER VARYING(200) NOT NULL,
    phone SERIAL,
    password CHARACTER VARYING(200) NOT NULL);"""

    conn = init_db()
    cur = conn.cursor()
    cur.execute(query)
    conn.commit()
    conn.close()
