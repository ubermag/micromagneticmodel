import pytest
import numbers
import numpy as np
import micromagneticmodel as mm


class TestZeeman:
    def setup(self):
        self.valid_args = [(1, 1.4, 1),
                           (0, 0, 1),
                           [1.2, 0, 0],
                           (0.56e6, 1.98e6, -1.1e7),
                           np.array([15e6, 0, 5e-8])]
        self.invalid_args = [(1, 1),
                             1,
                             (1.2, 0, 0, 5),
                             (0.56, 1.98, '-1.1'),
                             ([15], [0], [np.pi])]

    def test_init_valid_args(self):
        for H in self.valid_args:
            zeeman = mm.Zeeman(H)
            assert isinstance(zeeman.H, (tuple, list, np.ndarray))
            assert len(zeeman.H) == 3
            assert all([isinstance(i, numbers.Real) for i in zeeman.H])

    def test_init_invalid_args(self):
        for H in self.invalid_args:
            with pytest.raises(Exception):
                zeeman = mm.Zeeman(H)

    def test_repr_latex(self):
        for H in self.valid_args:
            zeeman = mm.Zeeman(H)
            latex = zeeman._repr_latex_()

            # Assert some characteristics of LaTeX string.
            assert latex[0] == latex[-1] == '$'
            assert latex[1] == '-'
            assert r'\mu_{0}' in latex
            assert r'\mathbf{H}' in latex
            assert r'\mathbf{m}' in latex
            assert r'\cdot' in latex
            assert r'M_\text{s}' in latex

    def test_name(self):
        for H in self.valid_args:
            zeeman = mm.Zeeman(H)
            assert zeeman.name == 'zeeman'

    def test_repr(self):
        for H in self.valid_args:
            zeeman = mm.Zeeman(H)
            assert repr(zeeman) == ('Zeeman(H={}, '
                                    'name=\'{}\')'.format(H, 'zeeman'))

        zeeman = mm.Zeeman(H=(1, 0, 1), name='test_name')
        assert repr(zeeman) == 'Zeeman(H=(1, 0, 1), name=\'test_name\')'

    def test_script(self):
        for H in self.valid_args:
            zeeman = mm.Zeeman(H)
            with pytest.raises(NotImplementedError):
                script = zeeman._script
