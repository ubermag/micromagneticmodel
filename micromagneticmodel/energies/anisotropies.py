from IPython.display import Math

class UniaxialAnisotropy(object):
    def __init__(self, K, u):
        self.K = K
        self.u = u

        self.expression = 'K (\mathbf{m} \cdot \mathbf{u})^{2}'

    def show(self):
        return Math(self.expression)
