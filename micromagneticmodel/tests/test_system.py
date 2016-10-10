import pytest
import numpy as np
import discretisedfield as df
import micromagneticmodel as mm


class TestSystem:
    def setup(self):
        p1 = (0, 0, 0)
        p2 = (1., 1., 1.)
        cell = (0.2, 0.2, 0.2)

        self.mesh = df.Mesh(p1, p2, cell)

    def test_init(self):
        system = mm.System(name="test_sim")
        system.mesh = self.mesh

        assert system.mesh.p1 == (0, 0, 0)
        assert system.mesh.p2 == (1, 1, 1)
        assert system.mesh.cell == (0.2, 0.2, 0.2)
        assert system.mesh.centre() == (0.5, 0.5, 0.5)

        assert isinstance(system.hamiltonian, mm.Hamiltonian)
        assert system.hamiltonian.terms == []

        system.hamiltonian = mm.Exchange(1e-12) + mm.Demag()
        assert len(system.hamiltonian.terms)

        assert isinstance(system.dynamics, mm.Dynamics)
        assert system.dynamics.terms == []

        assert system.name == "test_sim"

    def test_wrong_kwargs(self):
        with pytest.raises(AttributeError):
            system = mm.System(name="wrong_mesh", attr="a")

    def test_invalid_mesh(self):
        with pytest.raises(TypeError):
            system = mm.System(mesh="a", name="wrong_mesh")

    def test_set_m(self):
        m_list = [(0, 0.1, 0),
                  (1, 0, 0),
                  (0, 1, 0),
                  (0, 0, 1),
                  [1, 2, 3],
                  np.array([0, 1, 2]),
                  df.Field(self.mesh, dim=3, value=(0, 0, 1))]

        system = mm.System(mesh=self.mesh, name="test_sim")

        for m in m_list:
            system.m = m

            assert isinstance(system.m, df.Field)
            assert len(system.m.average()) == 3

    def test_set_wrong_m(self):
        system = mm.System(mesh=self.mesh, name="test_sim")

        with pytest.raises(TypeError):
            system.m = "a"

    def test_set_hamiltonian_with_energyterm(self):
        system = mm.System()
        assert isinstance(system.hamiltonian, mm.Hamiltonian)
        system.hamiltonian = mm.Exchange(1e-12)
        assert isinstance(system.hamiltonian, mm.Hamiltonian)
        assert len(system.hamiltonian.terms) == 1

    def test_set_hamiltonian_wrong(self):
        system = mm.System()
        assert isinstance(system.hamiltonian, mm.Hamiltonian)
        with pytest.raises(TypeError):
            system.hamiltonian = 1

    def test_set_dynamics_with_dynamicsterm(self):
        system = mm.System()
        assert isinstance(system.dynamics, mm.Dynamics)
        system.dynamics = mm.Precession(2.211e5)
        assert isinstance(system.dynamics, mm.Dynamics)
        assert len(system.dynamics.terms) == 1

    def test_set_dynamics_wrong(self):
        system = mm.System()
        assert isinstance(system.dynamics, mm.Dynamics)
        with pytest.raises(TypeError):
            system.dynamics = 1

    def test_script(self):
        system = mm.System(mesh=self.mesh, name="test_sim")

        with pytest.raises(NotImplementedError):
            system.script()
