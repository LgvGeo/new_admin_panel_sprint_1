import os
import sqlite3
from contextlib import contextmanager

import psycopg2
from dotenv import load_dotenv
from psycopg2.extensions import connection as _connection
from psycopg2.extras import DictCursor

from db_controllers import PGController, SqliteController
from models import FilmWork, Genre, GenreFilmWork, Person, PersonFilmWork

load_dotenv()
psycopg2.extras.register_uuid()

LOADING_SIZE = 10000


@contextmanager
def sqlite_conntection(db_path: str):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    yield conn
    conn.close()


def load_from_sqlite(sqlite_conn: sqlite3.Connection, pg_conn: _connection):
    """Основной метод загрузки данных из SQLite в Postgres"""
    sqlite_controller = SqliteController(sqlite_conn)
    pg_controller = PGController(pg_conn)
    for data in sqlite_controller.extract_filmwork(LOADING_SIZE):
        pg_controller.load_to_db(FilmWork, data)
    for data in sqlite_controller.extract_genre(LOADING_SIZE):
        pg_controller.load_to_db(Genre, data)
    for data in sqlite_controller.extract_person(LOADING_SIZE):
        pg_controller.load_to_db(Person, data)
    for data in sqlite_controller.extract_genre_film_work(LOADING_SIZE):
        pg_controller.load_to_db(GenreFilmWork, data)
    for data in sqlite_controller.extract_person_film_work(LOADING_SIZE):
        pg_controller.load_to_db(PersonFilmWork, data)


if __name__ == '__main__':
    dsl = {
        'dbname': os.environ.get('DB_NAME'),
        'user': os.environ.get('DB_USER'),
        'password': os.environ.get('DB_PASSWORD'),
        'host': os.environ.get('DB_HOST'),
        'port': os.environ.get('DB_PORT')
    }
    with (sqlite_conntection('db.sqlite') as sqlite_conn,
          psycopg2.connect(**dsl, cursor_factory=DictCursor) as pg_conn):
        load_from_sqlite(sqlite_conn, pg_conn)
