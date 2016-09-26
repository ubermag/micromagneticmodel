import pytest
from micromagneticmodel import System
from micromagneticmodel.drivers import MinDriver


class TestMinDriver:
    def setup(self):
        system = System()
        self.driver = MinDriver(system)

    def test_init(self):
        assert isinstance(self.driver.system, System)
