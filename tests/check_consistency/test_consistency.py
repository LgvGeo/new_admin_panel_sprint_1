import dateutil.parser


class TestConsistency:
    def check_consistency(
        self, pg_cursor, sqlite_cursor,
        table_name, fields, is_created_field, is_modified_field
    ):
        list_sqlite = sqlite_cursor.execute(
            f'SELECT id, {fields} FROM {table_name} order by id;').fetchall()
        pg_cursor.execute(
            f'SELECT id, {fields} FROM content.{table_name} order by id;')
        list_pg = pg_cursor.fetchall()
        assert list_pg == list_sqlite

        if is_created_field:
            created_list_sqlite = [
                (dateutil.parser.isoparse(created[0]),)
                for created in sqlite_cursor.execute(
                    f'SELECT created_at AS created'
                    f' FROM {table_name} order by id'
                ).fetchall()
            ]
            pg_cursor.execute(
                f'SELECT created FROM content.{table_name} order by id')
            created_list_pg = pg_cursor.fetchall()
            assert created_list_sqlite == created_list_pg
        if is_modified_field:
            modified_list_sqlite = [
                (dateutil.parser.isoparse(modified[0]),)
                for modified in sqlite_cursor.execute(
                    f'SELECT updated_at AS updated '
                    f'FROM {table_name} order by id').fetchall()]
            pg_cursor.execute(
                f'SELECT modified FROM content.{table_name} order by id')
            modified_list_pg = pg_cursor.fetchall()
            assert modified_list_pg == modified_list_sqlite

    def check_count(self, pg_cursor, sqlite_cursor, table_name):
        count_sqlite = sqlite_cursor.execute(
            f'Select count(*) from {table_name};').fetchone()
        pg_cursor.execute(f'Select count(*) from content.{table_name};')
        count_pg = pg_cursor.fetchone()

        assert count_sqlite == count_pg

    def test_genre_count(self, pg_cursor, sqlite_cursor):
        self.check_count(pg_cursor, sqlite_cursor, 'genre')

    def test_filmwork_count(self, pg_cursor, sqlite_cursor):
        self.check_count(pg_cursor, sqlite_cursor, 'film_work')

    def test_person_count(self, pg_cursor, sqlite_cursor):
        self.check_count(pg_cursor, sqlite_cursor, 'person')

    def test_genre_filmwork_count(self, pg_cursor, sqlite_cursor):
        self.check_count(pg_cursor, sqlite_cursor, 'genre_film_work')

    def test_person_filmwork_count(self, pg_cursor, sqlite_cursor):
        self.check_count(pg_cursor, sqlite_cursor, 'person_film_work')

    def test_filmwork_consistency(self, pg_cursor, sqlite_cursor):
        self.check_consistency(
            pg_cursor, sqlite_cursor,
            'film_work',
            'title, description, rating, type',
            True, True)

    def test_person_consistency(self, pg_cursor, sqlite_cursor):
        self.check_consistency(
            pg_cursor, sqlite_cursor,
            'person', 'full_name', True, True)

    def test_genre_consistency(self, pg_cursor, sqlite_cursor):
        self.check_consistency(
            pg_cursor, sqlite_cursor,
            'genre', 'name, description',
            True, True)

    def test_genre_filmwork_consistency(self, pg_cursor, sqlite_cursor):
        self.check_consistency(
            pg_cursor, sqlite_cursor,
            'genre_film_work', 'genre_id, film_work_id',
            True, False)

    def test_person_filmwork_consistency(self, pg_cursor, sqlite_cursor):
        self.check_consistency(
            pg_cursor, sqlite_cursor,
            'person_film_work', 'person_id, film_work_id',
            True, False)
