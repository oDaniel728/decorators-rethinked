from typing import Callable, Generic, ParamSpec, TypeVar

P = ParamSpec("P")
R = TypeVar("R")
class decorator(Generic[P, R]):
    def __init__(self, func: Callable[P, R]):
        self.__wrapper = func

    def __call__(self, *args: P.args, **kwargs: P.kwargs) -> R:
        return self.__wrapper(*args, **kwargs)
    
    def __rmatmul__(self, *args: P.args, **kwargs: P.kwargs) -> R:
        return self.__wrapper(*args, **kwargs)

__all__ = ['decorator']