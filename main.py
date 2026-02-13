import builtins
from typing import Any, Iterable, Literal, Type, TypeGuard, TypedDict
import typing

from decorator import decorator, Callable

@decorator
def say(self: str) -> None: # prints itself
    # "foo" @say
    # print("foo")
    print(self)

@decorator
def tostr(self: Any) -> str: # converts itself into a str
    # 1 @tostr
    # str(1)
    return str(self)

def round(precision: int):
    # 1.2345 @round(2) -> 1.23
    # round(1.2345, 2) -> 1.23
    @decorator
    def wrapper(self: float) -> float:
        return builtins.round(self, precision)
    return wrapper

def concat(other: str):
    # 'foo' @concat('bar') -> 'foobar'
    # 'foo' + 'bar'
    @decorator
    def wrapper(self: str) -> str:
        return self + other
    return wrapper

def join(other: str):
    # [1, 2, 3] @join('-') -> '1-2-3'
    # '-'.join([1, 2, 3]) -> '1-2-3'
    @decorator
    def wrapper(self: Iterable[Any]) -> str:
        return other.join(map(str, self))
    return wrapper

def cast[T](typ: Type[T] | T = None):
    # 1.0 @cast(int) -> (int) 1
    # int(1.0) -> 1
    @decorator
    def wrapper(self: Any) -> T:
        return typing.cast(typ, self) # type: ignore
    
    return wrapper

@decorator
def secure[R](self: Callable[[], R]) -> R | None:
    # [() -> T] method @secure -> (T | None)
    # try: method(); except: return None
    try: return self()
    except Exception: return None

def onlyif[R](condition: Callable[[], bool] | bool):
    # [() -> T] method @onlyif(bool) -> (T | None)
    # if (bool): method()
    # roda a função apenas se condition for verdadeira
    @decorator
    def wrapper(self: Callable[[], R]) -> R | None:
        if isinstance(condition, bool): return self() if condition else None
        elif callable(condition): return self() if condition() else None
    return wrapper

class _ReturnDict[T](TypedDict):
    type: Literal['ret']
    value: T

@decorator
def ret[T](self: T) -> _ReturnDict[T]:
    return {'type': 'ret', 'value': self}

@decorator
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
            
            if isinstance(output, dict) and output.get('type') == 'ret':
                output = output['value']
            r.append(output)
        return r
    return out

def foreach[T](fn: Callable[[T, int], Any]):
    @decorator
    def wrapper(self: Iterable[T]):
        for i, v in enumerate(self):
            fn(v, i)
    return wrapper

def choose[T, U](i: U, default: T) -> decorator[[Iterable[tuple[T, U]]], T]:
    @decorator
    def wrapper(self: Iterable[tuple[T, U]]) -> T:
        for v, k in self:
            if k == i: return v
        return default
    return wrapper

@decorator
def encapsulate[T](self: T) -> Callable[[], T]:
    return lambda: self

main = (
    range(1,11) @foreach([
        lambda I, i: (
            n:=f'{I}º',
            n:=[
                ('primeira', 1), 
                ('segunda', 2), 
                ('terça', 3), 
                ('quarta', 4), 
                ('quinta', 5)
            ] @choose(I, n),
            f"Olá pela {n} vez!" @say,
            None @ret
        )
    ] @compose)
    @cast(None)
    @encapsulate
) @secure @encapsulate
main @onlyif(__name__ == "__main__")