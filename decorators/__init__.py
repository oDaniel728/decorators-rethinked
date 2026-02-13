from typing import Callable, Generic, ParamSpec, TypeVar

P = ParamSpec("P")
R = TypeVar("R")
def decorator() -> 'Callable[[Callable[P, R]], Decorator[P, R]]':
    def wrapper(func):
        return Decorator(func)
    return wrapper
class Decorator(Generic[P, R]):
    def __init__(self, func: Callable[P, R]):
        self.__wrapper = func

    def __call__(self, *args: P.args, **kwargs: P.kwargs) -> R:
        return self.__wrapper(*args, **kwargs)
    
    def __rmatmul__(self, *args: P.args, **kwargs: P.kwargs) -> R:
        return self.__wrapper(*args, **kwargs)
