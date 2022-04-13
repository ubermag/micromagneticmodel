import discretisedfield as df
import ubermagutil.typesystem as ts

import micromagneticmodel as mm


@ts.typesystem(
    m=ts.Typed(expected_type=df.Field, allow_none=True),
    T=ts.Scalar(unsigned=True),
    name=ts.Name(const=True),
)
class System:
    """System class.

    This class is used for defining a micromagnetic system. In order to
    uniquely define a micromagnetic system, the following parameters can be
    provided:

    - Energy equation (``system.energy``)
    - Dynamics equation  (``system.dynamics``)
    - Magnetisation field (``system.m``)
    - Temperature (``system.T``)
    - Name (``system.name``)

    Parameters
    ----------
    energy : micromagneticmodel.Energy, optional

        Energy equation. Defaults to 0.

    dynamics : micromagneticmodel.Dynamics, optional

        Dynamics equation. Defaults to 0.

    m : disretisedfield.Field, optional

        Magnetisation field. Defaults to ``None``.

    T : numbers.Real

        Temperature. Defaults to 0.

    name : str, optional

        Name of the system. Defaults to ``'unnamed'``.

    Examples
    --------
    1. Defining a system.

    >>> import micromagneticmodel as mm
    >>> import discretisedfield as df
    ...
    >>> p1 = (0, 0, 0)
    >>> p2 = (10e-9, 10e-9, 10e-9)
    >>> n = (5, 5, 5)
    >>> region = df.Region(p1=p1, p2=p2)
    >>> mesh = df.Mesh(region=region, n=n)
    >>> m = df.Field(mesh, dim=3, value=(0, 0, 1), norm=1e6)
    >>> energy = mm.Exchange(A=1e-11) + mm.Demag()
    >>> dynamics = mm.Precession(gamma0=mm.consts.gamma0) + \
            mm.Damping(alpha=0.1)
    >>> T = 0
    >>> name = 'my_cool_system'
    >>> system = mm.System(energy=energy,
    ...                    dynamics=dynamics,
    ...                    m=m,
    ...                    T=T,
    ...                    name=name)

    """

    def __init__(self, energy=0, dynamics=0, m=None, T=0, name="unnamed"):
        self.energy = energy
        self.dynamics = dynamics
        self.m = m
        self.T = T
        self.name = name

        # Newly created system has not been "driven" yet.
        self.drive_number = 0
        self.compute_number = 0

    @property
    def energy(self):
        """Energy equation of the system.

        Parameters
        ----------
        value : micromagneticmodel.Energy, micromagneticmodel.EnergyTerm

            Energy container/term of the system.

        Returns
        -------
        micromagneticmodel.Energy

            Energy container of the system.

        Examples
        --------
        1. System's energy equation.

        >>> import micromagneticmodel as mm
        ...
        >>> system = mm.System(name='my_cool_system')
        >>> repr(system.energy)  # energy not set yet
        'Energy()'
        >>> system.energy = mm.Exchange(A=1e-12)
        >>> repr(system.energy)
        'Exchange(A=1e-12)'
        >>> system.energy += mm.Demag()
        >>> repr(system.energy)
        'Exchange(A=1e-12) + Demag()'

        .. seealso:: :py:func:`~micromagneticmodel.System.dynamics`

        """
        return self._energy

    @energy.setter
    def energy(self, value):
        empty_container = mm.Energy()
        if value == 0:
            self._energy = empty_container
        elif isinstance(value, (mm.EnergyTerm, mm.Energy)):
            self._energy = empty_container + value  # checks by + operator
        else:
            msg = f"Cannot set energy equation with {type(value)}."
            raise TypeError(msg)

    @property
    def dynamics(self):
        """Dynamics equation of the system.

        Parameters
        ----------
        value : micromagneticmodel.Dynamics, micromagneticmodel.DynamicsTerm

            Dynamics container/term of the system.

        Returns
        -------
        micromagneticmodel.Dynamics

            Dynamics container of the system.

        Examples
        --------
        1. System's dynamics equation.

        >>> import micromagneticmodel as mm
        ...
        >>> system = mm.System(name='my_cool_system')
        >>> repr(system.dynamics)  # energy not set yet
        'Dynamics()'
        >>> system.dynamics = mm.Damping(alpha=0.001)
        >>> repr(system.dynamics)
        'Damping(alpha=0.001)'
        >>> system.dynamics += mm.Precession(gamma0=2.21e5)
        >>> repr(system.dynamics)
        'Damping(alpha=0.001) + Precession(gamma0=221000.0)'

        .. seealso:: :py:func:`~micromagneticmodel.System.energy`

        """
        return self._dynamics

    @dynamics.setter
    def dynamics(self, value):
        empty_container = mm.Dynamics()
        if value == 0:
            self._dynamics = empty_container
        elif isinstance(value, (mm.DynamicsTerm, mm.Dynamics)):
            self._dynamics = empty_container + value  # checks by + operator
        else:
            msg = f"Cannot set dynamics equation with {type(value)}."
            raise TypeError(msg)

    def __repr__(self):
        """Representation string.

        Returns
        -------
        str

            Representation string.

        Examples
        --------
        1. Getting representation string.

        >>> import micromagneticmodel as mm
        ...
        >>> system = mm.System(name='my_cool_system')
        >>> repr(system)
        "System(name='my_cool_system')"

        """
        return f"System(name='{self.name}')"
