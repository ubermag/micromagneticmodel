from IPython.display import Math


class Dynamics(object):
    def __init__(self):
        self.terms = []

    def add(self, term):
        self.terms.append(term)

    def show(self):
        expression = '\\frac{\partial \mathbf{m}}{\partial t}='

        for term in self.terms:
            string = term.expression
            if string[0] != '-' and expression[-1] != '=':
                expression += '+'
            expression += term.expression

        if len(self.terms) == 0:
            expression += '0'

        return Math(expression)
