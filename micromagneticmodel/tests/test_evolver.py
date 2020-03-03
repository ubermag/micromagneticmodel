import pytest
import micromagneticmodel as mm


class MyEvolver(mm.Evolver):
    _allowed_attributes = ['arg1', 'arg2']


def test_init():
    evolver = MyEvolver(arg1=1, arg2='abc')
    assert evolver.arg1 == 1
    assert evolver.arg2 == 'abc'

    with pytest.raises(AttributeError):
        evolver = MyEvolver(arg1=1, arg2='abc', arg3=3)  # arg3 is not allowed
