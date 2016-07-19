import six
import abc


@six.add_metaclass(abc.ABCMeta)
class TermSum(object):
    _latex_str = ''

    def __init__(self):
        self.terms = []

    @property
    def latex_str(self):
        self._latex_str = self._lefthandside

        for i in self.terms:
            if i._latex_str[1] != '-' and self._latex_str[-1] != '=':
                self._latex_str += '+'
            self._latex_str += i._latex_str[1:-1]

        if self.terms == []:
            self._latex_str += '0'
        self._latex_str += '$'

        return self._latex_str

    def _repr_latex_(self):
        return self.latex_str

    @abc.abstractmethod
    def add(self, term): pass

    @abc.abstractmethod
    def _lefthandside(self): pass
    
    def __iadd__(self, other):
        self.add(other)
        return self

    def calculator_script(self):
        script = ''
        for term in self.terms:
            script += term.calculator_script()

        return script
