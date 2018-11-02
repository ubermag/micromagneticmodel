import pytest
import numbers
import micromagneticmodel as mm


class TestDamping:
    def setup(self):
        self.valid_args = [1, 2.0, 5e-11, 1e-12, 1e-13, 1e-14, 1e6]
        self.invalid_args = [-1, -2.1, 'a', (1, 2), -3.6e-6, '0', [1, 2, 3]]

    def test_init_valid_args(self):
        for alpha in self.valid_args:
            damping = mm.Damping(alpha)

            assert damping.alpha == alpha
            assert isinstance(damping.alpha, numbers.Real)

    def test_init_invalid_args(self):
        for alpha in self.invalid_args:
            with pytest.raises(Exception):
                damping = mm.Damping(alpha)

    def test_repr_latex_(self):
        for alpha in self.valid_args:
            damping = mm.Damping(alpha)
            latex = damping._repr_latex_()

            # Assert some characteristics of LaTeX string.
            assert isinstance(latex, str)
            assert latex[0] == latex[-1] == '$'
            assert r'\alpha' in latex
            assert r'\mathbf{m}' in latex
            assert r'\frac' in latex
            assert r'\times' in latex
            assert latex.count(r'\partial') == 2

    def test_name(self):
        for alpha in self.valid_args:
            damping = mm.Damping(alpha)
            assert damping.name == 'damping'

    def test_repr(self):
        for alpha in self.valid_args:
            damping = mm.Damping(alpha)
            assert repr(damping) == ('Damping(alpha={}, '
                                     'name=\'damping\')').format(alpha)

        damping = mm.Damping(alpha=0.05, name='test_name')
        assert repr(damping) == 'Damping(alpha=0.05, name=\'test_name\')'

    def test_script(self):
        for alpha in self.valid_args:
            damping = mm.Damping(alpha)
            with pytest.raises(NotImplementedError):
                script = damping._script
