from micromagneticmodel.energies import DemagAbstract


class Demag(DemagAbstract):
    """Implementation of the abstract class for testing."""
    def calculator_script(self):
        raise NotImplementedError()


class TestExchangeAbstract(object):
    def test_repr_latex_(self):
        demag = Demag()
        latex_str = demag._repr_latex_()

        # Assert some characteristics of LaTeX string.
        assert isinstance(latex_str, str)
        assert latex_str[0] == latex_str[-1] == '$'
        assert '\\mu_{0}' in latex_str
        assert '\mathbf{H}_\\text{d}' in latex_str
        assert '\mathbf{m}' in latex_str
        assert '\cdot' in latex_str
        assert 'M_\\text{s}' in latex_str
        assert '\\frac{1}{2}' in latex_str
