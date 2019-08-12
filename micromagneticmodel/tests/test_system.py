import pytest
import numpy as np
import discretisedfield as df
import micromagneticmodel as mm


class TestSystem:
    def setup(self):
        p1 = (0, 0, 0)
        p2 = (1., 1., 1.)
        cell = (0.2, 0.2, 0.2)
        self.mesh = df.Mesh(p1=p1, p2=p2, cell=cell)

    def test_init(self):
        system = mm.System(name="test_sim")

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

    def test_set_m(self):
        system = mm.System(name="test_sim")

        system.m = df.Field(self.mesh, dim=3, value=(0, 0, 1))

        assert isinstance(system.m, df.Field)
        assert len(system.m.average) == 3

    def test_set_wrong_m(self):
        system = mm.System(name="test_sim")

        with pytest.raises(TypeError):
            system.m = "a"

    def test_set_hamiltonian_with_energyterm(self):
        system = mm.System()
        assert isinstance(system.hamiltonian, mm.Hamiltonian)
        system.hamiltonian = mm.Exchange(1e-12)
        assert isinstance(system.hamiltonian, mm.Hamiltonian)
        assert len(system.hamiltonian.terms) == 1

    def test_set_hamiltonian_with_zero(self):
        system = mm.System()
        system.hamiltonian = mm.Exchange(1e-12) + mm.Demag()
        assert isinstance(system.hamiltonian, mm.Hamiltonian)
        assert len(system.hamiltonian.terms) == 2

        system.hamiltonian = 0
        assert isinstance(system.hamiltonian, mm.Hamiltonian)
        assert len(system.hamiltonian.terms) == 0

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

    def test_set_dynamics_with_zero(self):
        system = mm.System()
        system.dynamics = mm.Precession(2e5) + mm.Damping(0.1)
        assert isinstance(system.dynamics, mm.Dynamics)
        assert len(system.dynamics.terms) == 2

        system.dynamics = 0
        assert isinstance(system.dynamics, mm.Dynamics)
        assert len(system.dynamics.terms) == 0

    def test_set_dynamics_wrong(self):
        system = mm.System()
        assert isinstance(system.dynamics, mm.Dynamics)
        with pytest.raises(TypeError):
            system.dynamics = 1

    def test_script(self):
        system = mm.System(name="test_sim")

        with pytest.raises(NotImplementedError):
            script = system._script

    def test_repr(self):
        # 'empty' system object
        system = mm.System()
        r = repr(system)
        assert 'hamiltonian' in r
        assert 'dynamics' in r
        assert 'System' in r

        # system object with name
        system = mm.System(name='testname')
        r = repr(system)
        assert 'testname' in r
