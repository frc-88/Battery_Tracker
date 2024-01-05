from __future__ import annotations
from abc import ABC, abstractmethod, abstractclassmethod


class GenericEntry(ABC):
    @abstractclassmethod
    def from_bytes(cls, data: bytes) -> GenericEntry:
        pass

    @abstractclassmethod
    def length(cls) -> int:
        pass
