import pytest
import numbers
import micromagneticmodel as mm


class TestSTT(object):
    def setup(self):
        self.valid_args = [((1, -2, 3), 1),
                           ((-1.0, 0, 1e-6), 2.0),
                           ((0, 0, 0), 5e-11),
                           ((11, 2, 19), -1e-12)]
        self.invalid_args = [((1, -2), 1),
                             ((-1.0, 0, 1e-6), "2.0"),
                             ((0, 0, 0, 9), 5e-11),
                             ((11, 2, 19), -1e-12+2j)]

    def test_init_valid_args(self):
        for arg in self.valid_args:
            u, beta = arg
            stt = mm.STT(u, beta)

            assert stt.u == u
            assert isinstance(stt.u, tuple)
            assert stt.beta == beta
            assert isinstance(stt.beta, numbers.Real)

    def test_init_invalid_args(self):
        for arg in self.invalid_args:
            u, beta = arg
            
            with pytest.raises(Exception):
                stt = mm.STT(gamma)

    def test_repr_latex_(self):
        for arg in self.valid_args:
            u, beta = arg
            stt = mm.STT(u, beta)
            latex_str = stt._repr_latex_()

            # Assert some characteristics of LaTeX string.
            assert isinstance(latex_str, str)
            assert latex_str[0] == latex_str[-1] == '$'
            assert '\\beta' in latex_str
            assert '\mathbf{m}' in latex_str
            assert '\mathbf{u}' in latex_str
            assert '\\times' in latex_str
            assert '\\boldsymbol' in latex_str
            assert '\\nabla' in latex_str

    def test_name(self):
        for arg in self.valid_args:
            u, beta = arg
            stt = mm.STT(u, beta)

            assert stt.name == 'stt'

    def test_repr(self):
        for arg in self.valid_args:
            u, beta = arg
            stt = mm.STT(u, beta)

            assert repr(stt) == "STT(u={}, beta={})".format(u, beta)
            
        stt = mm.STT((1, 2, 3), 15)
        assert repr(stt) == 'STT(u=(1, 2, 3), beta=15)'

    def test_script(self):
        for arg in self.valid_args:
            u, beta = arg
            stt = mm.STT(u, beta)
            with pytest.raises(NotImplementedError):
                stt.script()
