import sqlite3
from pathlib import Path
from typing import TypeVar, Any

T = TypeVar('T')
K = TypeVar('K')
V = TypeVar('V')


def values(d: dict[K, V]) -> list[V]:
    return list(d.values())


def dict_factory(cursor: sqlite3.Cursor, row: sqlite3.Row) -> dict[str, Any]:
    fields = [column[0] for column in cursor.description]
    return {key: value for key, value in zip(fields, row)}


class Database:

    def __init__(self, db_file_path: str) -> None:
        print(f'{db_file_path=}')
        self.con = sqlite3.connect(db_file_path, autocommit=True)
        self.con.row_factory = dict_factory

        db_ver = values(self.con.execute('pragma user_version').fetchone())[0]
        if db_ver == 0:
            self._init_database()

        if values(self.con.execute('pragma user_version').fetchone())[0] != 1:
            raise Exception('Could not init database.')

    def _init_database(self) -> None:
        self.con.executescript(Path('schema.sql').read_text('utf-8'))
        self.con.execute('pragma user_version = 1')
