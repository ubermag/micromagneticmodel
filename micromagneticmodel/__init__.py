from .consts import mu0, e, muB, kB
import micromagneticmodel.util  # to avoid import order conflicts
from .hamiltonian import EnergyTerm, Exchange, \
    UniaxialAnisotropy, Demag, Zeeman, Hamiltonian
from .dynamics import DynamicsTerm, Precession, \
    Damping, STT, Dynamics
from .drivers import Driver, MinDriver, TimeDriver
from .system import System


def test():
    import pytest  # pragma: no cover
    pytest.main(["-v", "--pyargs", "micromagneticmodel"])  # pragma: no cover
