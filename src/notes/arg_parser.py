import argparse


def make_argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument('--db_file_path', required=True, type=str,
                        help="The path to the SQLite database to store progress in. If the file does not exist it will be created.")
    parser.add_argument('--pass_note_avg_millis', required=True, type=int, default=5_000,
                        help="The average number of milliseconds per note to pass a level.")
    parser.add_argument('--curr_grp', required=False, type=int, default=1,
                        help="The group number to start from.")
    return parser
