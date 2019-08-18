import pytest
import micromagneticmodel as mm


class MyDriver(mm.Driver):
    _allowed_kwargs = ['arg1', 'arg2']

    
def test_init():
    driver = MyDriver(arg1=1, arg2='abc')
    assert driver.arg1 == 1
    assert driver.arg2 == 'abc'
    
    with pytest.raises(AttributeError):
        driver = MyDriver(arg1=1, arg2='abc', arg3=3)


def test_script():
    driver = mm.Driver()
    with pytest.raises(NotImplementedError):
        script = driver._script


def test_drive():
    driver = mm.Driver()
    with pytest.raises(NotImplementedError):
        script = driver.drive()
