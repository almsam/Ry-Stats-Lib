from typing import Any, Callable, Concatenate
import functools

__all__ = ("copy_callable_signature", "copy_method_signature")

def copy_callable_signature[T, **P](
    source: Callable[P, T]
) -> Callable[[Callable[..., T]], Callable[P, T]]:
    def wrapper(target: Callable[..., T]) -> Callable[P, T]:
        @functools.wraps(source)
        def wrapped(*args: P.args, **kwargs: P.kwargs) -> T:
            return target(*args, **kwargs)

        return wrapped

    return wrapper

def copy_method_signature[T, **P](
    source: Callable[Concatenate[Any, P], T]
) -> Callable[[Callable[..., T]], Callable[Concatenate[Any, P], T]]:
    def wrapper(target: Callable[..., T]) -> Callable[Concatenate[Any, P], T]:
        @functools.wraps(source)
        def wrapped(self: Any, /, *args: P.args, **kwargs: P.kwargs) -> T:
            return target(self, *args, **kwargs)

        return wrapped

    return wrapper