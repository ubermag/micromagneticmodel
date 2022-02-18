"""Domain-specific language for computational magnetism."""
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

__version__ = pkg_resources.get_distribution(__name__).version


def test():
    """Run all package tests.

    Examples
    --------
    1. Run all tests.

    >>> import micromagneticmodel
    ...
    >>> # micromagneticmodel.test()

    """
    return pytest.main(['-v', '--pyargs',
                        'micromagneticmodel', '-l'])  # pragma: no cover
