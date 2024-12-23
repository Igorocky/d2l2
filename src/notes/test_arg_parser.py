from io import StringIO
from unittest import TestCase

from arg_parser import make_argument_parser


class CommonTest(TestCase):
    def test__make_argument_parser__parses_arguments(self) -> None:
        # given
        parser = make_argument_parser()

        # when
        args = parser.parse_args([
            '--db_file_path', '/usr/data/note.sqlite',
            '--curr_grp', '3',
            '--pass_note_avg_millis', '1500'
        ])

        # then
        self.assertEqual('/usr/data/note.sqlite', args.db_file_path)
        self.assertEqual(3, args.curr_grp)
        self.assertEqual(1500, args.pass_note_avg_millis)

    def test__make_argument_parser__returns_default_values_for_optional_arguments(self) -> None:
        # given
        parser = make_argument_parser()

        # when
        args = parser.parse_args([
            '--db_file_path', '/usr/data/note.sqlite',
            '--pass_note_avg_millis', '2000'
        ])

        # then
        self.assertEqual('/usr/data/note.sqlite', args.db_file_path)
        self.assertEqual(1, args.curr_grp)
        self.assertEqual(2000, args.pass_note_avg_millis)

    def test__make_argument_parser__prints_help(self) -> None:
        # given
        parser = make_argument_parser()
        help_output = StringIO()

        # when
        parser.print_help(help_output)

        # then
        self.assertEqual(
        """usage: _jb_unittest_runner.py [-h] --db_file_path DB_FILE_PATH
                              --pass_note_avg_millis PASS_NOTE_AVG_MILLIS
                              [--curr_grp CURR_GRP]

options:
  -h, --help            show this help message and exit
  --db_file_path DB_FILE_PATH
                        The path to the SQLite database to store progress in.
                        If the file does not exist it will be created.
  --pass_note_avg_millis PASS_NOTE_AVG_MILLIS
                        The average number of milliseconds per note to pass a
                        level.
  --curr_grp CURR_GRP   The group number to start from.
""",
            help_output.getvalue()
        )
