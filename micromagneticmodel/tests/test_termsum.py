import pytest
import micromagneticmodel as mm


class TestTermSum:
    def test_abstract_class(self):
        with pytest.raises(TypeError):
                termsum = mm.util.TermSum()
