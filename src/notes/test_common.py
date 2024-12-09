from unittest import TestCase

from common import group_by_octaves, note_to_str, arrange_groups_for_learning
from staff import get_all_notes, Clef


class CommonTest(TestCase):
    def test_group_by_octaves(self) -> None:
        bass_grps = group_by_octaves([n for c, n in get_all_notes() if c == Clef.BASS])
        bass_grps_str = [[note_to_str(n) for n in g] for g in bass_grps]
        self.assertEqual(
            [
                ['1D', '1E', '1F', '1G', '1A', '1B'],
                ['2C', '2D', '2E', '2F', '2G', '2A', '2B'],
                ['3C', '3D', '3E', '3F', '3G', '3A', '3B'],
                ['4C', '4D', '4E', '4F', '4G', '4A', '4B', '5C', '5D']
            ],
            bass_grps_str
        )
        treble_grps = group_by_octaves([n for c, n in get_all_notes() if c == Clef.TREBLE])
        treble_grps_str = [[note_to_str(n) for n in g] for g in treble_grps]
        self.assertEqual(
            [
                ['2B', '3C', '3D', '3E', '3F', '3G', '3A', '3B'],
                ['4C', '4D', '4E', '4F', '4G', '4A', '4B'],
                ['5C', '5D', '5E', '5F', '5G', '5A', '5B'],
                ['6C', '6D', '6E', '6F', '6G', '6A', '6B']
            ],
            treble_grps_str
        )

    def test_arrange_groups_for_learning(self) -> None:
        self.assertEqual(
            [[0], [1], [0, 1], [2], [3], [2, 3], [0, 1, 2, 3]],
            arrange_groups_for_learning(4)
        )
        self.assertEqual(
            [[0], [1], [0, 1], [2], [0, 1, 2], [3], [4], [3, 4], [0, 1, 2, 3, 4]],
            arrange_groups_for_learning(5)
        )
        self.assertEqual(
            [[0], [1], [0, 1], [2], [0, 1, 2], [3], [4], [3, 4], [5], [3, 4, 5], [0, 1, 2, 3, 4, 5]],
            arrange_groups_for_learning(6)
        )
