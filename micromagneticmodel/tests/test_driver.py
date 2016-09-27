import pytest
from micromagneticmodel.drivers import Driver


class TestDriver:
    def setup(self):
        self.driver = Driver(a=1, b=2, c='c')

    def test_init(self):
        assert self.driver.a == 1
        assert self.driver.b == 2
        assert self.driver.c == "c"
        
    def test_drive(self):
        with pytest.raises(NotImplementedError):
            self.driver.drive()

    def test_script(self):
        with pytest.raises(NotImplementedError):
            self.driver.script()
