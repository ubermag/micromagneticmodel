class Driver:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def drive(self):
        raise NotImplementedError

    def script(self):
        raise NotImplementedError

    def run_simulator(self):
        raise NotImplementedError

    def update_system(self):
        raise NotImplementedError
