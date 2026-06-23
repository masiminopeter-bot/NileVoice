from abc import ABC, abstractmethod
from typing import Generic, TypeVar

T = TypeVar("T")


class BaseService(ABC, Generic[T]):
    @abstractmethod
    def create(self, data: T) -> T:
        raise NotImplementedError

    @abstractmethod
    def retrieve(self, obj_id: int) -> T | None:
        raise NotImplementedError

    @abstractmethod
    def list(self) -> list[T]:
        raise NotImplementedError

    @abstractmethod
    def delete(self, obj_id: int) -> None:
        raise NotImplementedError
