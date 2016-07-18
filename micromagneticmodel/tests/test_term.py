import pytest
from micromagneticmodel.util import Term


class TestTerm(object):
    def test_abstract_class(self):
        with pytest.raises(TypeError):
                term = Term()
