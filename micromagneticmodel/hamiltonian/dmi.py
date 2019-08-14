import discretisedfield as df
import ubermagutil.typesystem as ts
from .energyterm import EnergyTerm


@ts.typesystem(D=ts.Parameter(descriptor=ts.Scalar(),
                              otherwise=df.Field),
               crystalclass=ts.InSet(allowed_values={'cnv', 't',
                                                     'o', 'd2d',
                                                     'interfacial'}),
               name=ts.Name(constant=True))
class DMI(EnergyTerm):
    def __init__(self, D, crystalclass='t', name='dmi', **kwargs):
        """Micromagnetic Dzyaloshinskii-Moriya (DM) energy term.

        This object models micromagnetic Dzyaloshinskii-Moriya energy
        term. It takes the DM energy constant `D` and crystallographic
        class `crystalclass`, and `name` as input parameters. In
        addition, any further parameters, required by a specific
        micromagnetic calculator can be passed.

        Parameters
        ----------
        D : int, float, dict, discretisedfield.Field
            A single positive value (int, float) can be
            passed. Alternatively, if it is defined per region, a
            dictionary can be passed, e.g. `A={'region1': 1e-12,
            'region2': 5e-12}`. If it is possible to define the
            parameter "per cell", `discretisedfield.Field` can be
            passed.
        crystalclass : str
            One of the following classes is allowed: `'Cnv'`, `'T'`,
            `'O'`, `'D2d'`, or `'interfacial'`.
        name : str
            Name of the energy term.

        Examples
        --------
        1. Initialising the Dzyaloshinskii-Moriya energy term.

        >>> import micromagneticmodel as mm
        ...
        >>> dmi1 = mm.DMI(D=1e-3, crystalclass='Cnv')
        >>> dmi2 = mm.DMI(D={'r1': 1e-3, 'r2': 2e-3},
        ...               crystalclass='D2d')
        >>> mesh = df.Mesh(p1=(0, 0, 0), p2=(5e-9, 5e-9, 5e-9),
        ...                cell=(1e-9, 1e-9, 1e-9))
        >>> field = df.Field(mesh, dim=1, value=1e12)
        >>> dmi3 = mm.DMI(D=field, crystalclass='T')

        """
        self.D = D
        self.crystalclass = crystalclass.lower()
        self.name = name
        self.__dict__.update(kwargs)

    @property
    def _latex(self):
        if self.crystalclass in ['t', 'o']:
            return r'$D \mathbf{m} \cdot (\nabla \times \mathbf{m})$'
        elif self.crystalclass in ['cnv', 'interfacial']:
            return (r'$D ( \mathbf{m} \cdot \nabla m_{z} '
                    r'- m_{z} \nabla \cdot \mathbf{m} )$')
        else:
            return (r'$D\mathbf{m} \cdot \left( \frac{\partial '
                    r'\mathbf{m}}{\partial x} \times \hat{x} - '
                    r'\frac{\partial \mathbf{m}}{\partial y} '
                    r'\times \hat{y} \right)$')

    @property
    def _repr(self):
        """A representation string property.

        Returns:
           A representation string.

        """
        return (f'DMI(D={self.D}, crystalclass=\'{self.crystalclass}\', '
                f'name=\'{self.name}\')')
