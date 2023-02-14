from jittok import Callable as jCallable


class ConcreteCallable(jCallable[int, str]):
    def __call__(self, x: int) -> str:
        return str(x)


def test_jittok_callable_is_callable() -> None:
    sut = ConcreteCallable()
    assert callable(sut)
