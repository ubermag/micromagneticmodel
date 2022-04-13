import micromagneticmodel as mm


def test_version():
    assert isinstance(mm.__version__, str)
    assert "." in mm.__version__
