import micromagneticmodel as mm


def test_macrospin():
    assert isinstance(mm.examples.macrospin(), mm.System)
