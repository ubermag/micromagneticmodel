import numbers

import micromagneticmodel as mm


def test_consts():
    consts = ["mu0", "e", "me", "kB", "h", "g", "hbar", "gamma", "muB", "gamma0"]
    for const in consts:
        assert hasattr(mm.consts, const)
        assert isinstance(getattr(mm.consts, const), numbers.Real)
