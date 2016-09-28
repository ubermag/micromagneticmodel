import pytest
import micromagneticmodel as mm


class TestTimeDriver:
    def setup(self):
        self.td = mm.TimeDriver(t=1e-9, n=100)

    def test_init(self):
        assert self.td.t == 1e-9
        assert self.td.n == 100
