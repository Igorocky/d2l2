import datetime
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
        self._db_file_path = db_file_path
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

    def backup(self) -> None:
        curr_db_file_path = Path(self._db_file_path)
        curr_db_dir_path = curr_db_file_path.absolute().parent
        curr_db_file_name = curr_db_file_path.stem
        curr_db_file_ext = curr_db_file_path.suffix
        backup_dir_path_str = str(curr_db_dir_path) + '/backups'
        backup_dir_path = Path(backup_dir_path_str)
        if not backup_dir_path.exists():
            raise Exception(f'The backup directory doesn\'t exist: {backup_dir_path_str}')
        curr_time = datetime.datetime.now()
        curr_time_str = curr_time.strftime('%Y_%m_%d__%H_%M_%S')
        backup_db_file_path = f'{backup_dir_path_str}/{curr_db_file_name}__{curr_time_str}{curr_db_file_ext}'
        bkp_con = sqlite3.connect(backup_db_file_path)
        self.con.backup(bkp_con)
        bkp_con.close()
