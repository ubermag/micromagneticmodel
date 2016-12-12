class Driver:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def drive(self):
        raise NotImplementedError

    @property
    def script(self):
        raise NotImplementedError
