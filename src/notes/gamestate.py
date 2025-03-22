from dataclasses import dataclass, field
import random
from typing import Tuple

from common import group_by_octaves, arrange_groups_for_learning, note_to_str, str_to_note
from staff import get_all_notes
from staff import Clef


@dataclass
class State:
    started: bool = False
    show_keyboard: bool = False
    all_question_groups: list[list[Tuple[Clef, int]]] = field(default_factory=lambda: [])
    curr_grp: int = 0
    remaining_questions: list[Tuple[Clef, int]] = field(default_factory=lambda: [])
    cycle_started_at:int = 0
    notes_answered_in_cur_cycle:int = 0
    note_avg_millis_in_cur_cycle:int = -1
    note_avg_millis_best:int = -1
    mistakes_in_cur_cycle:int = 0
    pass_note_avg_millis:int = 0
    asked_at: int = 0
    first_ans: int | None = None

def make_state_for_groups(clefs:list[Clef], pass_note_avg_millis:int, curr_grp:int = 0) -> State:
    octaves:list[list[Tuple[Clef,int]]] = []
    for clef in clefs:
        all_notes = [n for c,n in get_all_notes() if c == clef]
        octaves_for_clef:list[list[int]] = group_by_octaves(all_notes)
        octaves.extend([[(clef,n) for n in octave] for octave in octaves_for_clef])
    random.shuffle(octaves)
    octave_idxs = arrange_groups_for_learning(len(octaves))
    all_question_groups: list[list[Tuple[Clef, int]]] = []
    for question_grp in octave_idxs:
        all_question_groups.append([])
        for octave_idx in question_grp:
            all_question_groups[-1].extend(octaves[octave_idx])
    return State(
        all_question_groups = all_question_groups,
        pass_note_avg_millis = pass_note_avg_millis,
        curr_grp=curr_grp
    )

def make_state_for_octaves(octaves:list[Tuple[Clef,int]]) -> State:
    notes_to_ask:list[Tuple[Clef,int]] = []
    for clef,octave in octaves:
        octave_str = str(octave)
        for cl,note in get_all_notes():
            if clef == cl and octave_str == note_to_str(note)[0]:
                notes_to_ask.append((clef,note))
        if clef == Clef.TREBLE and octave == 3:
            notes_to_ask.append((clef,str_to_note('2B')))
        elif clef == Clef.BASS and octave == 4:
            notes_to_ask.append((clef,str_to_note('5C')))
            notes_to_ask.append((clef,str_to_note('5D')))
    all_question_groups: list[list[Tuple[Clef, int]]] = [notes_to_ask]
    return State(
        all_question_groups = all_question_groups,
        pass_note_avg_millis = 1,
        curr_grp=0
    )