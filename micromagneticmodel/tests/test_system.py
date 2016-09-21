import pytest
from discretisedfield import Mesh
from micromagneticmodel import System


class TestSystem:
    def setup(self):
        c1 = (0, 0, 0)
        c2 = (1., 1., 1.)
        d = (0.2, 0.2, 0.2)

        self.mesh = Mesh(c1, c2, d)
    
    def test_init(self):
        Ms = 8.6e5
        
        system = System(self.mesh, Ms, name='test_sim')

