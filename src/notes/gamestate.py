from dataclasses import dataclass, field
import random
from typing import Tuple

from common import group_by_octaves, arrange_groups_for_learning
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
    note_avg_millis_in_cur_cycle:int = 1000_000_000
    pass_note_avg_millis:int = 0
    asked_at: int = 0
    first_ans: int | None = None

def make_state(clef:Clef, pass_note_avg_millis:int) -> State:
    all_notes = [n for c,n in get_all_notes() if c == clef]
    octaves = group_by_octaves(all_notes)
    random.shuffle(octaves)
    octave_idxs = arrange_groups_for_learning(len(octaves))
    all_question_groups: list[list[Tuple[Clef, int]]] = []
    for question_grp in octave_idxs:
        all_question_groups.append([])
        for octave_idx in question_grp:
            all_question_groups[-1].extend([(clef,n) for n in octaves[octave_idx]])
    return State(
        all_question_groups = all_question_groups,
        pass_note_avg_millis = pass_note_avg_millis
    )