from IPython.display import Math

class Damping(object):
    def __init__(self, alpha=1):
        self.alpha = alpha

        self.expression = '\\alpha \mathbf{m} \\times \\frac{\partial \mathbf{m}}{\partial t}'

    def show(self):
        return Math(self.expression)
