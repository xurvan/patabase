import psycopg2


class Database(object):
    def __init__(self, server: str, user: str, password: str, database: str):
        self._con = psycopg2.connect(
            server=server,
            user=user,
            password=password,
            database=database)

    def _execute(self, cur, query, parameters=None):
        try:
            cur.execute(query, parameters)
        except Exception as e:
            self._con.rollback()
            raise e

    def _callproc(self, cur, func_name, parameters=None):
        try:
            cur.callproc(func_name, parameters)
        except Exception as e:
            self._con.rollback()
            raise e

    def perform(self, sql: str, *args: any) -> int:

        with self._con.cursor() as cur:
            self._execute(cur, sql, args)
            self._con.commit()

            return cur.rowcount

    def select(self, sql: str, *args: any) -> iter:
        with self._con.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            self._execute(cur, sql, args)
            rows = cur.fetchall()

        for row in rows:
            yield dict(row)

    def procedure(self, func_name: str, **parameters: any) -> int:
        with self._con.cursor() as cur:
            self._callproc(cur, func_name, parameters)
            self._con.commit()

            return cur.rowcount

    def function(self, func_name: str, **parameters: any) -> iter:
        with self._con.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            self._callproc(cur, func_name, parameters)
            rows = cur.fetchall()

        for row in rows:
            yield dict(row)