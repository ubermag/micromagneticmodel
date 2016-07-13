from IPython.display import Math

class Precession(object):
    def __init__(self, gamma=1):
        self.gamma = gamma

        self.expression = '\gamma \mathbf{m} \\times \mathbf{H}_\\text{eff}'

    def show(self):
        return Math(self.expression)
