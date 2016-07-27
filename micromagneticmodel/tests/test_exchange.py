import pytest
from numbers import Real
from micromagneticmodel.hamiltonian import Exchange


class TestExchange(object):
    def setup(self):
        self.valid_args = [1, 2.0, 5e-11, 1e-12, 1e-13, 1e-14, 1e6]
        self.invalid_args = [-1, -2.1, 'a', (1, 2), -3.6e-6, '0', [1, 2, 3]]

    def test_abstract_script_method(self):
        for A in self.valid_args:
            with pytest.raises(NotImplementedError):
                exchange = Exchange(A)
                exchange.script()

    def test_init_valid_args(self):
        for A in self.valid_args:
            exchange = Exchange(A)

            assert exchange.A == A
            assert isinstance(exchange.A, Real)

    def test_init_invalid_args(self):
        for A in self.invalid_args:
            with pytest.raises(ValueError):
                exchange = Exchange(A)

    def test_repr_latex_(self):
        for A in self.valid_args:
            exchange = Exchange(A)
            latex_str = exchange._repr_latex_()

            # Assert some characteristics of LaTeX string.
            assert isinstance(latex_str, str)
            assert latex_str[0] == latex_str[-1] == '$'
            assert '\\nabla' in latex_str
            assert 'A' in latex_str
            assert latex_str.count('+') == 2

    def test_name(self):
        for A in self.valid_args:
            exchange = Exchange(A)

            assert exchange._name == 'exchange'

    def test_repr(self):
        for A in self.valid_args:
            exchange = Exchange(A)

            assert repr(exchange) == 'Exchange(A={})'.format(A)

        exchange = Exchange(8.78e-12)
        assert repr(exchange) == "Exchange(A=8.78e-12)"

    def test_script(self):
        for A in self.valid_args:
            exchange = Exchange(A)
            with pytest.raises(NotImplementedError):
                exchange.script()
