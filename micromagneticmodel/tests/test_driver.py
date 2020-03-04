import pytest
import micromagneticmodel as mm


class MyDriver(mm.Driver):
    _allowed_attributes = ['arg1', 'arg2']

    def drive(self, system):  # A simple drive method
        return system


class TestDriver:
    def test_init(self):
        driver = MyDriver(arg1=1, arg2='abc')
        assert driver.arg1 == 1
        assert driver.arg2 == 'abc'

        with pytest.raises(AttributeError):
            driver = MyDriver(arg1=1, arg2='abc', arg3=3)  # arg3 not allowed

    def test_drive(self):
        driver = MyDriver()
        assert driver.drive(system=5) == 5
