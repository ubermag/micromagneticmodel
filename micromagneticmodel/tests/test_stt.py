import pytest
import numbers
import micromagneticmodel as mm


class TestSTT:
    def setup(self):
        self.valid_args = [((1, -2, 3), 1),
                           ((-1.0, 0, 1e-6), 2.0),
                           ((0, 0, 0), 5e-11),
                           ((11, 2, 19), -1e-12)]
        self.invalid_args = [((1, -2), 1),
                             ((-1.0, 0, 1e-6), '2.0'),
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
            latex = stt._repr_latex_()

            # Assert some characteristics of LaTeX string.
            assert isinstance(latex, str)
            assert latex[0] == latex[-1] == '$'
            assert r'\beta' in latex
            assert r'\mathbf{m}' in latex
            assert r'\mathbf{u}' in latex
            assert r'\times' in latex
            assert r'\boldsymbol' in latex
            assert r'\nabla' in latex

    def test_name(self):
        for arg in self.valid_args:
            u, beta = arg
            stt = mm.STT(u, beta)

            assert stt.name == 'stt'

    def test_repr(self):
        for arg in self.valid_args:
            u, beta = arg
            stt = mm.STT(u, beta)

            assert repr(stt) == ('STT(u={}, beta={}, '
                                 'name=\'stt\')'.format(u, beta))

        stt = mm.STT((1, 2, 3), 15, name='test_name')
        assert repr(stt) == 'STT(u=(1, 2, 3), beta=15, name=\'test_name\')'

    def test_script(self):
        for arg in self.valid_args:
            u, beta = arg
            stt = mm.STT(u, beta)
            with pytest.raises(NotImplementedError):
                script = stt._script
