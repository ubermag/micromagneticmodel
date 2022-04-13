import pytest

import micromagneticmodel as mm

from .checks import check_container


class TestDynamics:
    def setup(self):
        self.precession = mm.Precession(gamma0=2.21e5)
        self.damping = mm.Damping(alpha={"r1": 1, "r2": 0.5})
        self.zhangli = mm.ZhangLi(u=500, beta=0.2)

        self.terms = [self.precession, self.damping, self.zhangli]

        self.invalid_terms = [1, 2.5, 0, "abc", [3, 7], [self.precession, 5]]

    def test_init(self):
        # Init with terms list.
        container = mm.Dynamics(terms=self.terms)
        check_container(container)
        assert len(container) == 3

        # Empty terms list.
        container = mm.Dynamics()
        check_container(container)
        assert len(container) == 0

        # Add terms one by one.
        for i, term in enumerate(self.terms):
            container += term
            check_container(container)
            assert len(container) == i + 1
            assert isinstance(container, mm.Dynamics)

        # Create container as a sum of terms.
        container = self.precession + self.damping
        check_container(container)
        assert len(container) == 2

    def test_init_invalid_args(self):
        container = mm.Dynamics()
        for term in self.invalid_terms:
            with pytest.raises(TypeError):
                container += term

        check_container(container)
        assert len(container) == 0

    def test_add_sub(self):
        container1 = mm.Dynamics(terms=[self.precession, self.zhangli])
        container2 = mm.Dynamics(terms=[self.damping])
        container3 = mm.Dynamics(terms=[self.precession, self.damping])

        assert container1 != container2

        res = container1 + container2
        check_container(res)
        assert len(res) == 3
        assert container1 + container2 == container2 + container1

        res = container3 - container2
        check_container(res)
        assert len(res) == 1
        assert self.damping not in res
        with pytest.raises(ValueError):
            res -= self.damping

        assert res + self.damping == self.damping + res

        with pytest.raises(TypeError):
            res = container1 + 5

        with pytest.raises(TypeError):
            res = container1 - 5

    def test_repr(self):
        container = mm.Dynamics(terms=self.terms)
        check_container(container)

        assert isinstance(repr(container), str)
        assert "Precession" in repr(container)

        container -= container.precession

        assert "Precession" not in repr(container)

    def test_repr_latex(self):
        container = mm.Dynamics()
        check_container(container)
        latexstr = container._repr_latex_()
        assert latexstr == "$0$"

    def test_getattr(self):
        container = mm.Dynamics(terms=self.terms)
        check_container(container)

        assert isinstance(container.precession, mm.Precession)
        assert hasattr(container.precession, "gamma0")
        assert isinstance(container.damping, mm.Damping)
        assert hasattr(container.damping, "alpha")
        assert isinstance(container.zhangli, mm.ZhangLi)
        assert hasattr(container.zhangli, "u")
        assert hasattr(container.zhangli, "beta")

        # Try to get non-existing attribute.
        container -= self.damping
        check_container(container)
        with pytest.raises(AttributeError):
            container.damping

    def test_freestyle(self):
        container = self.damping + self.zhangli  # single term is not allowed
        check_container(container)
        assert "alpha" in container._repr_latex_()
        assert len(container) == 2
        assert mm.Damping() in container  # term of the same type present
        assert "damping" in dir(container)
        assert len(list(container)) == 2

        container -= mm.Damping()
        check_container(container)
        assert len(container) == 1
        assert mm.Damping() not in container
        assert self.damping not in container
        assert self.zhangli in container
        assert container.zhangli == self.zhangli

        container = self.precession + container
        check_container(container)
        assert len(container) == 2
