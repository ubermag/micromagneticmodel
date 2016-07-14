from IPython.display import Math

class Zeeman(object):
    def __init__(self, H):
        self.H = H

        self.expression = '- \mu_{0}M_\\text{s} \mathbf{m} \cdot \mathbf{H}'
        
    def set_H(self, H):
        self.H = H

    def show(self):
        return Math(self.expression)
