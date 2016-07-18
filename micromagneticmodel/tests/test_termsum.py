import pytest
from micromagneticmodel.util import TermSum


class TestTermSum(object):
    def test_abstract_class(self):
        with pytest.raises(TypeError):
                termsum = TermSum()
