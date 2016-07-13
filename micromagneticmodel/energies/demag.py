from IPython.display import Math

class Demag(object):
    def __init__(self):
        self.expression = 'w_\\text{d}'

    def show(self):
        return Math(self.expression)
