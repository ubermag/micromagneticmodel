import re

import pytest

import micromagneticmodel as mm

from .checks import check_term


class TestDemag:
    def test_init_valid_arg(self):
        term = mm.Demag()
        check_term(term)
        assert term.name == "demag"
        assert re.search(r"^Demag\(.*\)$", repr(term))

    def test_init_invalid_args(self):
        with pytest.raises(AttributeError):
            mm.Exchange(wrong=1)
