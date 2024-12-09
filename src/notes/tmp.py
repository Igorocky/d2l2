import json

from gamestate import make_state
from staff import Clef

state = make_state(clef=Clef.BASS, pass_note_avg_millis=3000)
print(json.dumps(state.all_question_groups))