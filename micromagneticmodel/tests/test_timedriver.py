import pytest
from micromagneticmodel import System
from micromagneticmodel.drivers import TimeDriver


class TestTimeDriver:
    def setup(self):
        system = System()
        self.driver = TimeDriver(system, t=1e-9, n=200, name="driver")

    def test_init(self):
        assert isinstance(self.driver.system, System)
        assert self.driver.name == "driver"
        assert self.driver.t == 1e-9
        assert self.driver.n == 200
