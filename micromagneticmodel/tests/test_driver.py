import pytest
import micromagneticmodel as mm


class MyDriver(mm.Driver):
    _allowed_attributes = ['arg1', 'arg2']

    def drive(self, system):
        return system


def test_init():
    driver = MyDriver(arg1=1, arg2='abc')
    assert driver.arg1 == 1
    assert driver.arg2 == 'abc'

    with pytest.raises(AttributeError):
        driver = MyDriver(arg1=1, arg2='abc', arg3=3)


def test_drive():
    driver = MyDriver()
    assert driver.drive(system=5) == 5
