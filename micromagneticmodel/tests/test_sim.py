import pytest
from discretisedfield.mesh import Mesh


@pytest.fixture
def mesh():
    from discretisedfield.mesh import Mesh
    cmin = (0, 0, 0)
    cmax = (1., 1., 1.)
    #d = (2, 2, 2)
    d = (0.2, 0.2, 0.2)

    mymesh = Mesh(cmin, cmax, d)

    return mymesh
    


def test_sim(mesh):
    from micromagneticmodel.sim import Sim
    Ms = 8.6e5

    sim = Sim(mesh, Ms, name='test_sim')
    assert sim

