import pytest
import micromagneticmodel as mm


class TestDemag:
    def test_repr_latex_(self):
        demag = mm.Demag()
        latex = demag._repr_latex_()

        # Assert some characteristics of LaTeX string.
        assert isinstance(latex, str)
        assert latex[0] == latex[-1] == '$'
        assert '\\mu_{0}' in latex
        assert '\mathbf{H}_\\text{d}' in latex
        assert '\mathbf{m}' in latex
        assert '\cdot' in latex
        assert 'M_\\text{s}' in latex
        assert '\\frac{1}{2}' in latex

    def test_name(self):
        demag = mm.Demag()
        assert demag.name == 'demag'

    def test_repr(self):
        demag = mm.Demag()
        assert repr(demag) == 'Demag(name=\"demag\")'

    def test_script(self):
        demag = mm.Demag()
        with pytest.raises(NotImplementedError):
            script = demag._script
