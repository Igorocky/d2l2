from common import group_by_octaves
from common import note_to_str
from staff import Clef
from staff import get_all_notes

grps = group_by_octaves([n for c, n in get_all_notes() if c == Clef.BASS])
grps_str = [[note_to_str(n) for n in g] for g in grps]
print(f'{grps_str=}')
