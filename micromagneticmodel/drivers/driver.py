class Driver(object):
    def __init__(self, system):
        raise NotImplementedError

    def drive(self):
        raise NotImplementedError

    def script(self):
        raise NotImplementedError

    def run_simulator(self):
        raise NotImplementedError

    def update_system(self):
        raise NotImplementedError
