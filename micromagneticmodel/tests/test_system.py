import pytest
import numpy as np
from discretisedfield import Mesh, Field
from micromagneticmodel import System
from micromagneticmodel.hamiltonian import Hamiltonian
from micromagneticmodel.dynamics import Dynamics
from micromagneticmodel.hamiltonian import Exchange, Demag


class TestSystem:
    def setup(self):
        c1 = (0, 0, 0)
        c2 = (1., 1., 1.)
        d = (0.2, 0.2, 0.2)

        self.mesh = Mesh(c1, c2, d)

    def test_init(self):
        system = System(name="test_sim")
        system.mesh = self.mesh

        assert system.mesh.c1 == (0, 0, 0)
        assert system.mesh.c2 == (1, 1, 1)
        assert system.mesh.d == (0.2, 0.2, 0.2)
        assert system.mesh.domain_centre() == (0.5, 0.5, 0.5)

        assert isinstance(system.hamiltonian, Hamiltonian)
        assert system.hamiltonian.terms == []

        system.hamiltonian = Exchange(1e-12) + Demag()
        assert len(system.hamiltonian.terms)

        assert isinstance(system.dynamics, Dynamics)
        assert system.dynamics.terms == []

        assert system.name == "test_sim"

    def test_wrong_kwargs(self):
        with pytest.raises(AttributeError):
            system = System(name="wrong_mesh", attr="a")

    def test_invalid_mesh(self):
        with pytest.raises(TypeError):
            system = System(mesh="a", name="wrong_mesh")

    def test_set_m(self):
        m_list = [(0, 0.1, 0),
                  (1, 0, 0),
                  (0, 1, 0),
                  (0, 0, 1),
                  [1, 2, 3],
                  np.array([0, 1, 2])]

        system = System(mesh=self.mesh, name="test_sim")

        for m in m_list:
            system.m = m

            assert isinstance(system.m, Field)
            for i in range(3):
                system.m.average()[i] == m[i]

    def test_set_wrong_m(self):
        system = System(mesh=self.mesh, name="test_sim")

        with pytest.raises(TypeError):
            system.m = "a"

    def test_total_energy(self):
        system = System(mesh=self.mesh, name="test_sim")

        with pytest.raises(NotImplementedError):
            system.total_energy()

    def test_script(self):
        system = System(mesh=self.mesh, name="test_sim")

        with pytest.raises(NotImplementedError):
            system.script()
