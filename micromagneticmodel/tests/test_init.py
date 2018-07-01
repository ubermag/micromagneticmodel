import micromagneticmodel as mm

def test_version():
    assert isinstance(mm.__version__, str)
    assert '.' in mm.__version__

def test_dependencies():
    assert isinstance(mm.__dependencies__, list)
    assert len(mm.__dependencies__) > 0
    
