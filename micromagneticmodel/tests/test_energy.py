import pytest

import micromagneticmodel as mm

from .checks import check_container


class TestEnergy:
    def setup(self):
        self.exchange = mm.Exchange(A=1e-12)
        self.zeeman = mm.Zeeman(H=(0, 0, 1.2e6))
        self.uniaxialanisotropy = mm.UniaxialAnisotropy(K=1e4, u=(0, 1, 0))
        self.demag = mm.Demag()
        self.dmi = mm.DMI(D=1e-3, crystalclass="T")
        self.cubicanisotropy = mm.CubicAnisotropy(
            K={"r1": 1e6, "r2": 5e6}, u1=(0, 0, 1), u2=(0, 1, 0)
        )

        self.terms = [
            self.exchange,
            self.zeeman,
            self.uniaxialanisotropy,
            self.demag,
            self.dmi,
            self.cubicanisotropy,
        ]

        self.invalid_terms = [1, 2.5, 0, "abc", [3, 7e-12], [self.exchange, 2]]

    def test_init(self):
        # Init with terms list.
        container = mm.Energy(terms=self.terms)
        check_container(container)
        assert len(container) == 6

        # Empty terms list.
        container = mm.Energy()
        check_container(container)
        assert len(container) == 0

        # Add terms one by one.
        for i, term in enumerate(self.terms):
            container += term
            check_container(container)
            assert len(container) == i + 1
            assert isinstance(container, mm.Energy)

        # Create container as a sum of terms.
        container = (
            self.exchange
            + self.zeeman
            + self.uniaxialanisotropy
            + self.demag
            + self.dmi
            + self.cubicanisotropy
        )
        check_container(container)
        assert len(container) == 6

    def test_init_invalid_args(self):
        container = mm.Energy()
        for term in self.invalid_terms:
            with pytest.raises(TypeError):
                container += term

        check_container(container)
        assert len(container) == 0

    def test_add_sub(self):
        container1 = mm.Energy(terms=[self.exchange, self.dmi])
        container2 = mm.Energy(terms=[self.zeeman, self.demag])
        container3 = mm.Energy(terms=[self.demag])

        assert container1 != container2

        res = container1 + container2
        check_container(res)
        assert len(res) == 4
        assert container1 + container2 == container2 + container1

        res = container2 - container3
        check_container(res)
        assert len(res) == 1
        assert self.demag not in res
        with pytest.raises(ValueError):
            res -= self.demag

        assert res + self.demag == self.demag + res

        with pytest.raises(TypeError):
            res = container1 + 5

        with pytest.raises(TypeError):
            res = container1 - 5

    def test_repr(self):
        container = mm.Energy(terms=self.terms)
        check_container(container)

        assert isinstance(repr(container), str)
        assert "Exchange" in repr(container)

        container -= container.exchange

        assert "Exchange" not in repr(container)

    def test_repr_latex(self):
        container = mm.Energy()
        check_container(container)
        latexstr = container._repr_latex_()
        assert latexstr == "$0$"

    def test_getattr(self):
        container = mm.Energy(terms=self.terms)
        check_container(container)

        assert isinstance(container.exchange, mm.Exchange)
        assert hasattr(container.exchange, "A")
        assert isinstance(container.zeeman, mm.Zeeman)
        assert hasattr(container.zeeman, "H")
        assert isinstance(container.uniaxialanisotropy, mm.UniaxialAnisotropy)
        assert hasattr(container.uniaxialanisotropy, "K")
        assert hasattr(container.uniaxialanisotropy, "u")
        assert isinstance(container.demag, mm.Demag)
        assert isinstance(container.cubicanisotropy, mm.CubicAnisotropy)
        assert hasattr(container.cubicanisotropy, "K")
        assert hasattr(container.cubicanisotropy, "u1")
        assert hasattr(container.cubicanisotropy, "u2")
        assert isinstance(container.dmi, mm.DMI)
        assert hasattr(container.dmi, "D")
        assert hasattr(container.dmi, "crystalclass")

        # Try to get non-existing attribute.
        container -= self.exchange
        check_container(container)
        with pytest.raises(AttributeError):
            container.exchange

    def test_freestyle(self):
        container = self.dmi + self.zeeman  # single term is not allowed
        check_container(container)
        assert "D" in container._repr_latex_()
        assert len(container) == 2
        assert mm.Zeeman(H=(0, 0, 1e6)) in container  # same type term present?
        assert "dmi" in dir(container)
        assert len(list(container)) == 2

        container -= mm.DMI(D=1e-3, crystalclass="T")
        check_container(container)
        assert len(container) == 1
        assert mm.DMI(D=1e-2, crystalclass="Cnv") not in container
        assert self.exchange not in container
        assert self.zeeman in container
        assert container.zeeman == self.zeeman

        container = self.demag + container
        check_container(container)
        assert len(container) == 2

    def test_same_class_terms(self):
        term1 = mm.UniaxialAnisotropy(K=1e6, u=(0, 0, 1))
        term2 = mm.UniaxialAnisotropy(K=2e6, u=(0, 1, 0))
        term3 = mm.UniaxialAnisotropy(K=2e6, u=(1, 0, 0), name="ua2")

        with pytest.raises(ValueError):
            container = term1 + term2

        container = term1 + term3
        check_container(container)
        assert len(container) == 2
        assert term1 in container
        assert term3 in container
        assert container.uniaxialanisotropy.K == 1e6
        assert container.ua2.K == 2e6

    def test_energy_and_energy_density(self):
        container = self.dmi + self.zeeman  # single term is not allowed

        with pytest.raises(NotImplementedError):
            container.energy(None)

        with pytest.raises(NotImplementedError):
            container.density(None)
