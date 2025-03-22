import json

from gamestate import make_state_for_groups
from staff import Clef

state = make_state_for_groups(clefs=[Clef.BASS, Clef.TREBLE], pass_note_avg_millis=3000)
print(state.all_question_groups)