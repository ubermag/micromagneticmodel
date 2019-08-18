import pytest
import micromagneticmodel as mm


class TestEvolver:
    def setup(self):
        self.evolver = mm.Evolver(a=1, b=2, c='c')

    def test_init(self):
        assert self.evolver.a == 1
        assert self.evolver.b == 2
        assert self.evolver.c == 'c'

    def test_script(self):
        with pytest.raises(NotImplementedError):
            script = self.evolver._script
