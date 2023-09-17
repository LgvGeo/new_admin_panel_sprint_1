import os
import sqlite3

import psycopg2
import pytest
from dotenv import load_dotenv

load_dotenv()


@pytest.fixture(scope='module')
def pg_conn():
    dsl = {
        'dbname': os.environ.get('DB_NAME'),
        'user': os.environ.get('DB_USER'),
        'password': os.environ.get('DB_PASSWORD'),
        'host': os.environ.get('DB_HOST'),
        'port': os.environ.get('DB_PORT')
    }
    pg_conn = psycopg2.connect(**dsl)
    yield pg_conn
    pg_conn.close()


@pytest.fixture(scope='module')
def sqlite_conn():
    sqlite_conn = sqlite3.connect('db.sqlite')
    yield sqlite_conn
    sqlite_conn.close()


@pytest.fixture
def pg_cursor(pg_conn):
    pg_cursor = pg_conn.cursor()
    yield pg_cursor


@pytest.fixture
def sqlite_cursor(sqlite_conn):
    sqlite_cursor = sqlite_conn.cursor()
    yield sqlite_cursor
