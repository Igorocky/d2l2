from dataclasses import dataclass, field
from typing import Tuple

from staff import Clef


@dataclass
class State:
    started: bool = False
    show_keyboard: bool = False
    questions: list[Tuple[Clef, int]] = field(default_factory=lambda: [])
    asked_at: int = 0
    first_ans: int | None = None
