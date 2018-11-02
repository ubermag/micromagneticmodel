import pytest
import numbers
import micromagneticmodel as mm


class TestDMI:
    def setup(self):
        self.valid_args = [-1, 2.0, 5e-11, -1e-12, 1e-13, 1e-14, -1e6]
        self.invalid_args = ['a', (1, 2), '0', [1, 2, 3]]

    def test_init_valid_args(self):
        for D in self.valid_args:
            dmi = mm.DMI(D)
            assert dmi.D == D
            assert isinstance(dmi.D, numbers.Real)

    def test_init_invalid_args(self):
        for D in self.invalid_args:
            with pytest.raises(Exception):
                dmi = mm.DMI(D)

    def test_repr_latex_(self):
        for D in self.valid_args:
            dmi = mm.DMI(D, crystalclass='T')
            latex = dmi._repr_latex_()

            # Assert some characteristics of LaTeX string.
            assert isinstance(latex, str)
            assert latex[0] == '$'
            assert latex[-1] == '$'
            assert 'D' in latex
            assert latex.count(r'\mathbf{m}') == 2

            dmi = mm.DMI(D, crystalclass='cnv')
            latex = dmi._repr_latex_()

            # Assert some characteristics of LaTeX string.
            assert isinstance(latex, str)
            assert latex[0] == latex[-1] == '$'
            assert r'\nabla' in latex
            assert 'D' in latex
            assert latex.count(r'\frac') == 0

            dmi = mm.DMI(D, crystalclass='d2d')
            latex = dmi._repr_latex_()

            # Assert some characteristics of LaTeX string.
            assert isinstance(latex, str)
            assert latex[0] == latex[-1] == '$'
            assert r'\partial' in latex
            assert r'\hat' in latex
            assert 'D' in latex
            assert latex.count(r'\frac') == 2

    def test_name(self):
        for D in self.valid_args:
            dmi = mm.DMI(D)
            assert dmi.name == 'dmi'

    def test_repr(self):
        for D in self.valid_args:
            dmi = mm.DMI(D, crystalclass='t')
            assert repr(dmi) == ('DMI(D={}, crystalclass=\'t\', '
                                 'name=\'{}\')').format(D, 'dmi')

            dmi = mm.DMI(D, crystalclass='d2d', name='test_name')
            assert repr(dmi) == ('DMI(D={}, crystalclass=\'d2d\', '
                                 'name=\'test_name\')').format(D)

    def test_script(self):
        for D in self.valid_args:
            dmi = mm.DMI(D)
            with pytest.raises(NotImplementedError):
                script = dmi._script
