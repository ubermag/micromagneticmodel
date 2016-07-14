import abc


class EnergyTerm(object):
    __metaclass__ = abc.ABCMeta
    
    @abc.abstractmethod
    def __init__(self): pass
    
    @abc.abstractmethod
    def calculator_script(self): pass

    @abc.abstractmethod
    def latex_str(self): pass
    
    def _repr_latex_(self):
        """A LaTeX representation method."""
        return self.latex_str
