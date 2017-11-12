from typing import List


class Difficulty():

    DIFFICULTY_EASY_ID = 1
    DIFFICULTY_MEDIUM_ID = 2
    DIFFICULTY_HARD_ID = 3
    DIFFICULTY_EXTRA_HARD_ID = 4

    def __init__(self, tick: float, score_multiplier: float, name: str, id: int):
        self.tick = tick
        self.score_multiplier = score_multiplier
        self.name = name
        self.id = id


def get_all_difficulties() -> List[Difficulty]:
    return [
        Difficulty(0.6, 1, "Easy", Difficulty.DIFFICULTY_EASY_ID),
        Difficulty(0.5, 2, "Medium", Difficulty.DIFFICULTY_MEDIUM_ID),
        Difficulty(0.2, 4, "Hard", Difficulty.DIFFICULTY_HARD_ID),
        Difficulty(0.1, 8, "Extra Hard", Difficulty.DIFFICULTY_EXTRA_HARD_ID),
    ]