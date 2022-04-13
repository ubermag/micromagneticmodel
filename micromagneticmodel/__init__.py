"""Domain-specific language for computational magnetism."""
import pkg_resources
import pytest

import micromagneticmodel.abstract
import micromagneticmodel.consts
import micromagneticmodel.examples

from .driver import Driver
from .dynamics import Damping, Dynamics, DynamicsTerm, Precession, Slonczewski, ZhangLi
from .energy import (
    DMI,
    RKKY,
    CubicAnisotropy,
    Demag,
    Energy,
    EnergyTerm,
    Exchange,
    MagnetoElastic,
    UniaxialAnisotropy,
    Zeeman,
)
from .evolver import Evolver
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
    return pytest.main(
        ["-v", "--pyargs", "micromagneticmodel", "-l"]
    )  # pragma: no cover
