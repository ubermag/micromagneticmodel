import pytest
import micromagneticmodel as mm


class TestDemag:
    def test_repr_latex_(self):
        demag = mm.Demag()
        latex = demag._repr_latex_()

        # Assert some characteristics of LaTeX string.
        assert isinstance(latex, str)

    def test_name(self):
        demag = mm.Demag()
        assert demag.name == 'demag'

    def test_repr(self):
        demag = mm.Demag()
        assert repr(demag) == 'Demag(name=\'demag\')'

    def test_script(self):
        demag = mm.Demag()
        with pytest.raises(NotImplementedError):
            script = demag._script
