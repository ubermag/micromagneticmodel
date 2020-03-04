import ubermagutil as uu
import discretisedfield as df
import ubermagutil.typesystem as ts
from .energyterm import EnergyTerm


@uu.inherit_docs
@ts.typesystem(D=ts.Parameter(descriptor=ts.Scalar(), otherwise=df.Field),
               crystalclass=ts.Subset(sample_set={'Cnv', 'T', 'O', 'D2d'},
                                      unpack=False))
class DMI(EnergyTerm):
    """Dzyaloshinskii-Moriya energy term.

    .. math::

        w_\\text{dmi}^\\text{T(O)} = D \\mathbf{m} \\cdot (\\nabla  \\times
        \\mathbf{m})

    .. math::

        w_\\text{dmi}^\\text{Cnv} = D ( \\mathbf{m} \\cdot \\nabla m_{z} -
        m_{z} \\nabla \\cdot \\mathbf{m} )

    .. math::

        w_\\text{dmi}^\\text{D2d} = D \\mathbf{m} \\cdot \\left(
        \\frac{\\partial \\mathbf{m}}{\\partial x} \\times \\hat{x} -
        \\frac{\\partial \\mathbf{m}}{\\partial y} \\times \\hat{y} \\right)

    Parameters
    ----------
    D : numbers.Real, dict, discretisedfield.Field

        If a single unsigned value ``numbers.Real`` is passed, a spatially
        constant parameter is defined. For a spatially varying parameter,
        either a dictionary, e.g. ``D={'region1': 1e-3, 'region2': 5e-3}`` (if
        the parameter is defined "per region") or ``discretisedfield.Field`` is
        passed.

    crystalclass : str

        One of the following crystalographic classes is allowed: ``'Cnv'``,
        ``'T'``, ``'O'``, or ``'D2d'``. Please note that this argument is
        case-sensitive.

    Examples
    --------
    1. Defining the DMI energy term using scalar.

    >>> import micromagneticmodel as mm
    ...
    >>> dmi = mm.DMI(D=1e-3, crystalclass='T')

    2. Defining the DMI energy term using dictionary.

    >>> dmi = mm.DMI(D={'region1': 1e-3, 'region2': 5e-3}, crystalclass='Cnv')

    3. Defining the DMI energy term using ``discretisedfield.Field``.

    >>> import discretisedfield as df
    ...
    >>> region = df.Region(p1=(0, 0, 0), p2=(5e-9, 5e-9, 5e-9))
    >>> mesh = df.Mesh(region=region, n=(5, 5, 5))
    >>> D = df.Field(mesh, dim=1, value=5.7e-3)
    >>> dmi = mm.DMI(D=D, crystalclass='D2d')

    4. An attempt to define the DMI energy term using a wrong value.

    >>> dmi = mm.DMI(D=(1, 0, 0), crystalclass='T')  # vector value
    Traceback (most recent call last):
    ...
    TypeError: ...

    """
    _allowed_attributes = ['D', 'crystalclass']

    @property
    def _reprlatex(self):
        if self.crystalclass in ['T', 'O']:
            return r'D \mathbf{m} \cdot (\nabla \times \mathbf{m})'
        elif self.crystalclass in ['Cnv']:
            return (r'D ( \mathbf{m} \cdot \nabla m_{z} '
                    r'- m_{z} \nabla \cdot \mathbf{m} )')
        else:
            return (r'D\mathbf{m} \cdot \left( \frac{\partial '
                    r'\mathbf{m}}{\partial x} \times \hat{x} - '
                    r'\frac{\partial \mathbf{m}}{\partial y} '
                    r'\times \hat{y} \right)')

    def effective_field(self, m):
        raise NotImplementedError
