import pytest
from micromagneticmodel.drivers import MinDriver


class TestMinDriver:
    def setup(self):
        self.md = MinDriver(mxHxm=0.01)

    def test_init(self):
        assert self.md.mxHxm == 0.01
