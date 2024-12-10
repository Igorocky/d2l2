import json

from gamestate import make_state
from staff import Clef

state = make_state(clefs=[Clef.BASS,Clef.TREBLE], pass_note_avg_millis=3000)
print(state.all_question_groups)