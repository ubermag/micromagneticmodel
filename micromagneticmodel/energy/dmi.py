import discretisedfield as df
import ubermagutil as uu
import ubermagutil.typesystem as ts

from .energyterm import EnergyTerm


@uu.inherit_docs
@ts.typesystem(
    D=ts.Parameter(descriptor=ts.Scalar(), otherwise=df.Field),
    crystalclass=ts.Subset(
        sample_set={
            "Cnv",
            "Cnv_x",
            "Cnv_y",
            "Cnv_z",
            "T",
            "O",
            "D2d",
            "D2d_x",
            "D2d_y",
            "D2d_z",
        },
        unpack=False,
    ),
)
class DMI(EnergyTerm):
    r"""Dzyaloshinskii-Moriya energy term.

    .. math::

        w^\text{T(O)} = D \mathbf{m} \cdot (\nabla  \times \mathbf{m})

    .. math::

        w_x^\text{Cnv} = D ( \mathbf{m} \cdot \nabla m_{x} - m_{x} \nabla
        \cdot \mathbf{m} )

    .. math::

        w_y^\text{Cnv} = D ( \mathbf{m} \cdot \nabla m_{y} - m_{y} \nabla
        \cdot \mathbf{m} )

    .. math::

        w_z^\text{Cnv} = D ( \mathbf{m} \cdot \nabla m_{z} - m_{z} \nabla
        \cdot \mathbf{m} )

    .. math::

        w_x^\text{D2d} = D \mathbf{m} \cdot \left( \frac{\partial
        \mathbf{m}}{\partial y} \times \hat{y} - \frac{\partial
        \mathbf{m}}{\partial z} \times \hat{z} \right)

    .. math::

        w_y^\text{D2d} = D \mathbf{m} \cdot \left( \frac{\partial
        \mathbf{m}}{\partial z} \times \hat{z} - \frac{\partial
        \mathbf{m}}{\partial x} \times \hat{x} \right)

    .. math::

        w_z^\text{D2d} = D \mathbf{m} \cdot \left( \frac{\partial
        \mathbf{m}}{\partial x} \times \hat{x} - \frac{\partial
        \mathbf{m}}{\partial y} \times \hat{y} \right)

    Parameters
    ----------
    D : numbers.Real, dict, discretisedfield.Field

        If a single unsigned value ``numbers.Real`` is passed, a spatially
        constant parameter is defined. For a spatially varying parameter,
        either a dictionary, e.g. ``D={'region1': 1e-3, 'region2': 5e-3}`` (if
        the parameter is defined "per region") or ``discretisedfield.Field`` is
        passed.

        *Note*: Initialisation with ``discretisedfield.Field`` is currently
        incompatible with OOMMF.

    crystalclass : str

        One of the following crystalographic classes is allowed: ``'Cnv_x'``,
        ``'Cnv_y``, ``Cnv_z``, ``'T'``, ``'O'``, ``D2d_x``, ``D2d_y``, or
        ``'D2d_z'``. Please note that this argument is case-sensitive.

    Examples
    --------
    1. Defining DMI energy term using a scalar.

    >>> import micromagneticmodel as mm
    ...
    >>> dmi = mm.DMI(D=1e-3, crystalclass='T')

    2. Defining DMI energy term using a dictionary.

    >>> D = {'region1': 1e-3, 'region2': 5e-3}
    >>> dmi = mm.DMI(D=D, crystalclass='Cnv_z')

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
    _allowed_attributes = ["D", "crystalclass"]

    @property
    def _reprlatex(self):
        if self.crystalclass in ["T", "O"]:
            return r"D \mathbf{m} \cdot (\nabla \times \mathbf{m})"
        elif "Cnv" in self.crystalclass:
            if self.crystalclass == "Cnv":
                direction = "z"
            else:
                direction = self.crystalclass[-1]
            return (
                r"D ( \mathbf{m} \cdot \nabla m_{" + direction + r"} "
                r"- m_{" + direction + r"} \nabla \cdot \mathbf{m} )"
            )
        else:
            if self.crystalclass == "D2d_x":
                dir1 = "y"
                dir2 = "z"
            elif self.crystalclass == "D2d_y":
                dir1 = "z"
                dir2 = "x"
            else:
                dir1 = "x"
                dir2 = "y"
            return (
                r"D\mathbf{m} \cdot \left( \frac{\partial "
                r"\mathbf{m}}{\partial "
                + dir1
                + r"} \times \hat{"
                + dir1
                + r"} - \frac{\partial \mathbf{m}}{\partial "
                + dir2
                + r"} \times \hat{"
                + dir2
                + r"} \right)"
            )

    def effective_field(self, m):
        raise NotImplementedError
