import pytest
import micromagneticmodel as mm


class TestMinDriver:
    def setup(self):
        self.md = mm.MinDriver(mxHxm=0.01)

    def test_init(self):
        assert self.md.mxHxm == 0.01
