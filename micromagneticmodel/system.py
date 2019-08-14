import importlib
import discretisedfield as df
import micromagneticmodel as mm
import ubermagutil.typesystem as ts


@ts.typesystem(name=ts.Name(const=True))
class System:
    _attributes = ['hamiltonian', 'dynamics', 'm', 'name']

    def __init__(self, **kwargs):
        """System class.

        This class is used for defining a micromagnetic system. In
        order to uniquely define a micromagnetic system, the following
        three parameters must be provided:

        - Hamiltonian
        - Dynamics equation
        - Initial magnetisation configuration

        In addition, `name` can be passed at initialisation.

        Parameters
        ----------
        hamiltonian : micromagneticmodel.Hamiltonian, optional
            Hamiltonian as a sum of different energy terms.
        dynamics : micromagneticmodel.Dynamics, optional
            Dynamics as a sum of different dynamics terms.
        m : disretisedfield.Field, optional
            Initial magnetisation configuration as a three-dimensional
            field.
        name : str, optional
            Name of the system.

        Raises
        ------
        AttributeError
            If a keyword argument which is not in the parameter list
            is passed.

        Examples
        --------
        1. Setting a simple system class

        >>> import micromagneticmodel as mm
        >>> import discretisedfield as df
        ...
        >>> p1 = (0, 0, 0)
        >>> p2 = (10e-9, 10e-9, 10e-9)
        >>> n = (5, 5, 5)
        >>> mesh = df.Mesh(p1=p1, p2=p2, n=n)
        >>> m = df.Field(mesh, dim=3, value=(0, 0, 1), norm=1e6)
        >>> hamiltonian = mm.Exchange(A=1e-11) + mm.Demag()
        >>> dynamics = mm.Precession(gamma=mm.consts.gamma0) + \
                mm.Damping(alpha=0.1)
        >>> system = mm.System(hamiltonian=hamiltonian,
        ...                    dynamics=dynamics,
        ...                    m=m,
        ...                    name='mysystem')

        """
        self._module = importlib.__import__(self.__class__.__module__)
        for key, value in kwargs.items():
            if key in System._attributes:
                setattr(self, key, value)
            else:
                raise AttributeError('Unexpected kwarg {}.'.format(key))

        if not hasattr(self, 'hamiltonian'):
            self.hamiltonian = 0
        if not hasattr(self, 'dynamics'):
            self.dynamics = 0
        self.drive_number = 0

    @property
    def hamiltonian(self):
        """Hamiltonian of the system.

        Returns
        -------
        micromagneticmodel.Hamiltonian
            Hamiltonian as a sum of energy terms.

        """
        return self._hamiltonian

    @hamiltonian.setter
    def hamiltonian(self, value):
        self._hamiltonian = self._module.Hamiltonian()
        setattr(self._hamiltonian, '_system', self)
        if value == 0:
            pass
        elif isinstance(value, (mm.EnergyTerm, mm.Hamiltonian)):
            self._hamiltonian += value
        else:
            raise TypeError(f'Unsupported type(value)={type(value)}')

    @property
    def dynamics(self):
        """Dynamics equation of the system.

        Returns
        -------
        micromagneticmodel.Dynamics
            Dynamics equation as a sum of dynamics terms.

        """
        return self._dynamics

    @dynamics.setter
    def dynamics(self, value):
        self._dynamics = self._module.Dynamics()
        setattr(self._dynamics, '_system', self)
        if value == 0:
            pass
        elif isinstance(value, (mm.DynamicsTerm, mm.Dynamics)):
            self._dynamics += value
        else:
            raise TypeError(f'Unsupported type(value)={type(value)}')

    @property
    def m(self):
        """Magnetisation configuration.

        Magnetisation configuration describes the state of the system.

        Returns
        -------
        discertisedfield.Field
            Magnetisation configuration.

        """
        return self._m

    @m.setter
    def m(self, value):
        if isinstance(value, df.Field):
            self._m = value
        else:
            raise TypeError('Unsupported type(m)={}'.format(type(value)))

    def __repr__(self):
        """Representation string.

        Returns
        -------
        str
            Representation string

        """
        return f'System(name=\'{self.name}\')'

    @property
    def _script(self):
        """This method should be implemented by a specific micromagnetic
        calculator.

        """
        raise NotImplementedError
