import ubermagutil.typesystem as ts
from .energyterm import EnergyTerm


@ts.typesystem(D=ts.Scalar,
               crystalclass=ts.InSet(allowed_values={'cnv', 't',
                                                     'o', 'd2d',
                                                     'interfacial'}),
               name=ts.Name(constant=True))
class DMI(EnergyTerm):
    def __init__(self, D, crystalclass='t', name='dmi'):
        """A DMI energy class.

        Args:
            D (Real): DMI energy constant (J/m**2)
            
            crystalclass (string): Type of crystal class.
            Possible values are:
                'cnv', 't', 'o', 'd2d', 'interfacial'

        """
        self.D = D
        self.crystalclass = crystalclass.lower()
        self.name = name

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
        return ('DMI(D={}, crystalclass=\'{}\', '
                'name=\'{}\')').format(self.D, self.crystalclass, self.name)
