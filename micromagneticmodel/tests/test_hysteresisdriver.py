import pytest
import micromagneticmodel as mm


class TestHysteresisDriver:
    def setup(self):
        self.hd = mm.HysteresisDriver(Hmin=(0, 0, 0), Hmax=(1, 1, 1), n=100)

    def test_init(self):
        assert self.hd.Hmin == (0, 0, 0)
        assert self.hd.Hmax == (1, 1, 1)
        assert self.hd.n == 100
