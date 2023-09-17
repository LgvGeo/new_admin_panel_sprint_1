from pydantic import BaseModel
from models import FilmWork, PersonFilmWork, GenreFilmWork, Genre, Person
import dateutil.parser


class PGController:
    def __init__(self, connection):
        self.connection = connection
        self.cursor = self.connection.cursor()
        self.cursor.execute('SET LOCAL search_path TO content')

    def load_from_db(self, table: BaseModel):
        pass

    def load_to_db(self, table: BaseModel, data: list[BaseModel]):
        cols = table.model_fields.keys()
        table_name = table.model_json_schema()['title']
        sql_stmt = (
            f'INSERT INTO {table_name} ({",".join(cols)}) '
            f'VALUES ({("%s," * len(cols)).rstrip(",")})'
        )
        for x in data:
            self.cursor.execute(sql_stmt, tuple(x.model_dump().values()))


class SqliteController:
    def __init__(self, connection):
        self.connection = connection

    def extract_filmwork(self, n) -> list[FilmWork]:
        curs = self.connection.cursor()
        curs.execute(
            'SELECT id, title, description,'
            ' creation_date, rating, type, created_at AS created,'
            ' updated_at AS modified FROM film_work;')
        while True:
            data = [
                FilmWork(
                    id=x['id'], title=x['title'],
                    description=x['description'],
                    creation_date=(
                        None if x['creation_date'] is None
                        else dateutil.parser.isoparse(x['creation_date'])
                    ),
                    rating=None if x['rating'] is None else float(x['rating']),
                    type=x['type'],
                    created=(
                        None if x['created'] is None
                        else dateutil.parser.isoparse(x['created'])
                    ),
                    modified=(
                        None if x['modified'] is None
                        else dateutil.parser.isoparse(x['modified'])
                    ),
                    ) for x in curs.fetchmany(n)]
            if not data:
                return
            yield data

    def extract_genre(self, n) -> list[Genre]:
        curs = self.connection.cursor()
        curs.execute(
            'SELECT id, name, description, '
            'created_at AS created, updated_at AS modified FROM genre;'
        )
        while True:
            data = [
                Genre(
                    id=x['id'], name=x['name'],
                    description=x['description'],
                    created=dateutil.parser.isoparse(x['created']),
                    modified=dateutil.parser.isoparse(x['modified'])
                ) for x in curs.fetchmany(n)
            ]
            if not data:
                return
            yield data

    def extract_person(self, n) -> list[Person]:
        curs = self.connection.cursor()
        curs.execute(
            'SELECT id, full_name, '
            'created_at AS created, updated_at AS modified FROM person;'
        )
        while True:
            data = [
                Person(
                    id=x['id'], full_name=x['full_name'],
                    created=dateutil.parser.isoparse(x['created']),
                    modified=dateutil.parser.isoparse(x['modified'])
                ) for x in curs.fetchmany(n)
            ]
            if not data:
                return
            yield data

    def extract_genre_film_work(self, n) -> list[GenreFilmWork]:
        curs = self.connection.cursor()
        curs.execute(
            'SELECT id, film_work_id, genre_id, '
            'created_at AS created FROM genre_film_work;'
        )
        while True:
            data = [
                GenreFilmWork(
                    id=x['id'],
                    film_work_id=x['film_work_id'], genre_id=x['genre_id'],
                    created=dateutil.parser.isoparse(x['created'])
                ) for x in curs.fetchmany(n)
            ]
            if not data:
                return
            yield data

    def extract_person_film_work(self, n) -> list[PersonFilmWork]:
        curs = self.connection.cursor()
        curs.execute(
            'SELECT id, film_work_id, person_id, '
            'created_at AS created, role FROM person_film_work;'
        )
        while True:
            data = [
                PersonFilmWork(
                    id=x['id'], film_work_id=x['film_work_id'],
                    person_id=x['person_id'],
                    created=dateutil.parser.isoparse(x['created']),
                    role=x['role']
                ) for x in curs.fetchmany(n)
            ]
            if not data:
                return
            yield data
