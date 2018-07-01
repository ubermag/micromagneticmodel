import pytest
import pkg_resources
from .consts import mu0, e, me, kB, h, g, hbar, gamma, muB, gamma0
import micromagneticmodel.util  # to avoid import order conflicts
from .hamiltonian import EnergyProperties, EnergyTerm, Exchange, \
    UniaxialAnisotropy, CubicAnisotropy, Demag, Zeeman, DMI, Hamiltonian
from .dynamics import DynamicsTerm, Precession, \
    Damping, STT, Dynamics
from .drivers import Driver, MinDriver, TimeDriver, HysteresisDriver
from .system import System
from .data import Data


def test():
    return pytest.main(["-v", "--pyargs", "micromagneticmodel"])  # pragma: no cover

__version__ = pkg_resources.get_distribution(__name__).version
__dependencies__ = pkg_resources.require(__name__)
