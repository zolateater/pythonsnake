from typing import Optional
from abc import ABC, abstractmethod
from .enums import ControllerEvent


class AbstractController(ABC):
    """
    Provides basic interface for reading game input events,
    such as pressing direction key, pressing menu key, etc.
    """

    @abstractmethod
    def read_action(self) -> Optional[ControllerEvent]:
        raise NotImplementedError('Please, override this method')

    def key_code_equals_to_char(self, code: int, char: str) -> bool:
        return code == ord(char) or code == ord(char.upper())
