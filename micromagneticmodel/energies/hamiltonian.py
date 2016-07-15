import energyterm as et


class Hamiltonian(object):
    _latex_str = ''

    def __init__(self):
        self.energyterms = []

    @property
    def latex_str(self):
        self._latex_str = '$\mathcal{H}='

        for i in self.energyterms:
            if i._latex_str[1] != '-' and self._latex_str[-1] != '=':
                self._latex_str += '+'
            self._latex_str += i._latex_str[1:-1]

        if self.energyterms == []:
            self._latex_str += '0'
        self._latex_str += '$'

        return self._latex_str

    def _repr_latex_(self):
        return self.latex_str

    def add(self, term):
        if not isinstance(term, et.EnergyTerm):
            raise TypeError('Only energy terms can be added to hamiltonian.')
        self.energyterms.append(term)
        # This is to trigger
        self._latex_str = ''

    def __iadd__(self, other):
        self.add(other)
        return self
