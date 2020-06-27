import pytest
import pkg_resources
import micromagneticmodel.abstract
import micromagneticmodel.consts
import micromagneticmodel.examples
from .energy import EnergyTerm, Exchange, Zeeman, UniaxialAnisotropy, \
    CubicAnisotropy, Demag, Zeeman, DMI, MagnetoElastic, RKKY, Energy
from .dynamics import DynamicsTerm, Precession, Damping, ZhangLi, \
    Slonczewski, Dynamics
from .evolver import Evolver
from .driver import Driver
from .system import System


def test():
    return pytest.main(['-v', '--pyargs',
                        'micromagneticmodel'])  # pragma: no cover


__version__ = pkg_resources.get_distribution(__name__).version
__dependencies__ = pkg_resources.require(__name__)
