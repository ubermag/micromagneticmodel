from IPython.display import Math

class Hamiltonian(object):
    def __init__(self):
        self.terms = []

    def add(self, energy):
        self.terms.append(energy)

    def show(self):
        expression = '\mathcal{H}='

        for term in self.terms:
            string = term.expression
            if string[0] != '-' and expression[-1] != '=':
                expression += '+'
            expression += term.expression

        if len(self.terms) == 0:
            expression += '0'

        return Math(expression)
