from abc import ABC, abstractmethod
from typing import Generic, TypeVar

T = TypeVar("T")


class BaseRepository(ABC, Generic[T]):
    @abstractmethod
    def add(self, obj: T) -> T:
        raise NotImplementedError

    @abstractmethod
    def get(self, obj_id: int) -> T | None:
        raise NotImplementedError

    @abstractmethod
    def list(self) -> list[T]:
        raise NotImplementedError

    @abstractmethod
    def remove(self, obj: T) -> None:
        raise NotImplementedError
