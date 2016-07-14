from IPython.display import Math

class Exchange(object):
    def __init__(self, A):
        self.A = A

        self.expression = 'A [(\\nabla m_{x})^{2} + (\\nabla m_{y})^{2} + (\\nabla m_{z})^{2}]'

    def show(self):
        return Math(self.expression)
