import pytest
import numpy as np
from discretisedfield import Mesh, Field
from micromagneticmodel import System
from micromagneticmodel.hamiltonian import Hamiltonian
from micromagneticmodel.dynamics import Dynamics


class TestSystem:
    def setup(self):
        c1 = (0, 0, 0)
        c2 = (1., 1., 1.)
        d = (0.2, 0.2, 0.2)

        self.mesh = Mesh(c1, c2, d)
    
    def test_init(self):
        Ms = 8.6e5
        
        system = System(self.mesh, Ms, name='test_sim')

        assert system.mesh.c1 == (0, 0, 0)
        assert system.mesh.c2 == (1, 1, 1)
        assert system.mesh.d == (0.2, 0.2, 0.2)
        assert system.mesh.domain_centre() == (0.5, 0.5, 0.5)

        assert system.Ms == Ms

        assert isinstance(system.hamiltonian, Hamiltonian)
        assert system.hamiltonian.terms == []

        assert isinstance(system.dynamics, Dynamics)
        assert system.dynamics.terms == []

        assert isinstance(system.m, Field)
        assert system.m.dim == 3
        assert system.m.average() == (0, 0, 0)

        assert system.name == 'test_sim'

    def test_set_m(self):
        m_list = [(0, 0.1, 0),
                  (1, 0, 0),
                  (0, 1, 0),
                  (0, 0, 1),
                  [1, 2, 3],
                  np.array([0, 1, 2])]

        system = System(self.mesh, 1, name='test_sim')

        for m in m_list:
            system.m = m

            assert isinstance(system.m, Field)
            for i in range(3):
                system.m.average()[i] == m[i]

    def test_set_wrong_m(self):
        system = System(self.mesh, 1, name='test_sim')

        with pytest.raises(TypeError):
            system.m = 'a'
