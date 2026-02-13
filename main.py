import builtins
from typing import Any, Iterable, Type, TypeGuard
import typing

from decorators import Decorator, decorator, Callable

@decorator()
def say(self: str) -> None:
    print(self)

@decorator()
def tostr(self: Any) -> str:
    return str(self)

def round(precision: int):
    @decorator()
    def wrapper(self: float) -> float:
        return builtins.round(self, precision)
    return wrapper

def concat(other: str):
    @decorator()
    def wrapper(self: str) -> str:
        return self + other
    return wrapper

def join(other: str):
    @decorator()
    def wrapper(self: Iterable[Any]) -> str:
        return other.join(map(str, self))
    return wrapper

def cast[T](typ: Type[T]):
    @decorator()
    def wrapper(self: Any) -> T:
        return typing.cast(typ, self) # type: ignore
    
    return wrapper

@decorator()
def secure[R](self: Callable[[], R]) -> R | None:
    try: return self()
    except Exception: return None

def onlyif[R](condition: Callable[[], bool] | bool):
    # roda a função apenas se condition for verdadeira
    @decorator()
    def wrapper(self: Callable[[], R]) -> R | None:
        if isinstance(condition, bool): return self() if condition else None
        elif callable(condition): return self() if condition() else None
    return wrapper

@decorator()
def compose[**P, R](self: Iterable[Callable[P, R]]) -> Callable[P, list[R]]:
    # @@ onde @@
    # n = [lambda: print("foo"), lambda: print("bar"), lambda: 1 + 1] @compose
    # 
    # @@ vira @@
    # def n():
    #   print("foo")
    #   print("bar")
    #   return 1 + 1
    def out(*args: P.args, **kwargs: P.kwargs) -> list[R]:
        r = []
        for f in self:
            output = f(*args, **kwargs)
            if isinstance(output, (list, tuple)): # [code, code, None] -> None
                output = output[-1]
            r.append(output)
        return r
    return out

def foreach[T](fn: Callable[[T, int], Any]):
    @decorator()
    def wrapper(self: Iterable[T]):
        for i, v in enumerate(self):
            fn(v, i)
    return wrapper

def choose[T, U](i: U, default: T) -> Decorator[[Iterable[tuple[T, U]]], T]:
    @decorator()
    def wrapper(self: Iterable[tuple[T, U]]) -> T:
        for v, k in self:
            if k == i: return v
        return default
    return wrapper

@onlyif(__name__ == "__main__")
def main():
    range(10) @foreach([
        lambda I, i: (
            n:=f"{i}º",
            n:=[
                ('primeira', 1), 
                ('segunda', 2), 
                ('terça', 3), 
                ('quarta', 4), 
                ('quinta', 5)
            ] @choose(i, n),
            f"Olá pela {n} vez!" @ say
        )
    ] @compose)