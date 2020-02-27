import pytest
import pkg_resources
import micromagneticmodel.util
import micromagneticmodel.consts
from .energy import EnergyTerm, Exchange, Zeeman, UniaxialAnisotropy, \
    CubicAnisotropy, Demag, Zeeman, DMI, Energy
from .dynamics import DynamicsTerm, Precession, Damping, ZhangLi, Dynamics
from .evolvers import Evolver
from .drivers import Driver
from .system import System


def test():
    return pytest.main(["-v", "--pyargs",
                        "micromagneticmodel"])  # pragma: no cover


__version__ = pkg_resources.get_distribution(__name__).version
__dependencies__ = pkg_resources.require(__name__)
