import pytest
import numpy as np
from discretisedfield import Mesh, Field
from micromagneticmodel import System
from micromagneticmodel.hamiltonian import Hamiltonian
from micromagneticmodel import Dynamics, Precession
from micromagneticmodel import Exchange, Demag


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
                  np.array([0, 1, 2]),
                  Field(self.mesh, dim=3, value=(0, 0, 1))]

        system = System(mesh=self.mesh, name="test_sim")

        for m in m_list:
            system.m = m

            assert isinstance(system.m, Field)
            assert len(system.m.average()) == 3

    def test_set_wrong_m(self):
        system = System(mesh=self.mesh, name="test_sim")

        with pytest.raises(TypeError):
            system.m = "a"

    def test_set_hamiltonian_with_energyterm(self):
        system = System()
        assert isinstance(system.hamiltonian, Hamiltonian)
        system.hamiltonian = Exchange(1e-12)
        assert isinstance(system.hamiltonian, Hamiltonian)
        assert len(system.hamiltonian.terms) == 1

    def test_set_hamiltonian_wrong(self):
        system = System()
        assert isinstance(system.hamiltonian, Hamiltonian)
        with pytest.raises(TypeError):
            system.hamiltonian = 1

    def test_set_dynamics_with_dynamicsterm(self):
        system = System()
        assert isinstance(system.dynamics, Dynamics)
        system.dynamics = Precession(2.211e5)
        assert isinstance(system.dynamics, Dynamics)
        assert len(system.dynamics.terms) == 1

    def test_set_dynamics_wrong(self):
        system = System()
        assert isinstance(system.dynamics, Dynamics)
        with pytest.raises(TypeError):
            system.dynamics = 1

    def test_total_energy(self):
        system = System(mesh=self.mesh, name="test_sim")

        with pytest.raises(NotImplementedError):
            system.total_energy()

    def test_script(self):
        system = System(mesh=self.mesh, name="test_sim")

        with pytest.raises(NotImplementedError):
            system.script()
