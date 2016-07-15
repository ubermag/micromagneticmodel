import pytest
from numbers import Real
from micromagneticmodel.hamiltonian import ExchangeAbstract


class Exchange(ExchangeAbstract):
    """Implementation of the abstract class for testing."""
    def calculator_script(self):
        raise NotImplementedError()


class TestExchangeAbstract(object):
    def setup(self):
        self.valid_args = [1, 2.0, 5e-11, 1e-12, 1e-13, 1e-14, 1e6]
        self.invalid_args = [-1, -2.1, 'a', (1, 2), -3.6e-6, '0', [1, 2, 3]]

    def test_init_valid_args(self):
        for A in self.valid_args:
            exchange = Exchange(A)

            assert exchange.A == A
            assert isinstance(exchange.A, Real)

    def test_init_invalid_args(self):
        # Invalid arguments (ValueError expected).
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
