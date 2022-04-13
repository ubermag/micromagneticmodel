import discretisedfield as df

import micromagneticmodel as mm


def macrospin():
    """Macrospin system example.

    Returns a macrospin example (a single discretisation cell) with the sample
    size ``(1e-9, 1e-9, 1e-9)``. Energy equation contains only Zeeman energy
    term with external magnetic field ``H=(0, 0, 1e6)``. Dynamics equation
    contains precession (``gamma0=mm.consts.gamma0``) and damping
    (``alpha=0.1``) terms. The saturation magnetisation is ``Ms=1e6`` and the
    initial magnetisation is ``m=(0, 1, 1)``. The name of the returned system
    is ``'macrospin'``.

    Returns
    -------
    micromagneticmodel.System

        Macrospin system.

    Examples
    --------
    1. Getting macrospin example system.

    >>> import micromagneticmodel as mm
    ...
    >>> mm.examples.macrospin()
    System(name='macrospin')

    """
    name = "macrospin"
    p1 = (0, 0, 0)
    p2 = (1e-9, 1e-9, 1e-9)
    n = (1, 1, 1)
    region = df.Region(p1=p1, p2=p2)
    mesh = df.Mesh(region=region, n=n)

    system = mm.System(name=name)
    system.energy = mm.Zeeman(H=(0, 0, 1e6))
    system.dynamics = mm.Precession(gamma0=mm.consts.gamma0) + mm.Damping(alpha=0.1)
    system.m = df.Field(mesh, dim=3, value=(0, 1, 1), norm=1e6)

    return system
