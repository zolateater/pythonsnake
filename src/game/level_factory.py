from typing import List
from .level import Level


class LevelFactory():

    @classmethod
    def get_level_collection(self) -> List[Level]:
        return []
