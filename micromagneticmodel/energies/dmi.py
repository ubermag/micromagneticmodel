from IPython.display import Math

class DMI(object):
    def __init__(self, D):
        self.D = D

        self.expression = 'D \mathbf{m} \cdot (\\nabla \\times \mathbf{m})'

    def show(self):
        return Math(self.expression)
