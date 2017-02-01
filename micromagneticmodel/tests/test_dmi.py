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
            print(D)
            with pytest.raises(Exception):
                dmi = mm.DMI(D)

    def test_repr_latex_(self):
        for D in self.valid_args:
            dmi = mm.DMI(D)
            latex = dmi._repr_latex_()

            # Assert some characteristics of LaTeX string.
            assert isinstance(latex, str)
            assert latex[0] == latex[-1] == '$'
            assert '\\nabla' in latex
            assert 'D' in latex
            assert latex.count('\mathbf{m}') == 2

    def test_name(self):
        for D in self.valid_args:
            dmi = mm.DMI(D)
            assert dmi.name == 'dmi'

    def test_repr(self):
        for D in self.valid_args:
            dmi = mm.DMI(D)
            assert repr(dmi) == 'DMI(D={})'.format(D)

        dmi = mm.DMI(8.78e-12)
        assert repr(dmi) == "DMI(D=8.78e-12)"

    def test_script(self):
        for D in self.valid_args:
            dmi = mm.DMI(D)
            with pytest.raises(NotImplementedError):
                script = dmi._script
