from abc import ABCMeta, abstractmethod
from typing import Generic, TypeVar

S = TypeVar("S")
T = TypeVar("T")


class Callable(Generic[S, T], metaclass=ABCMeta):
    @abstractmethod
    def __call__(self, args: S) -> T:
        ...
