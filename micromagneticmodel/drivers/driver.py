class Driver(object):
    def __init__(self, system):
        self.system = system

    def drive(self):
        raise NotImplementedError

    def script(self):
        raise NotImplementedError

    def run_simulator(self):
        raise NotImplementedError

    def update_system(self):
        raise NotImplementedError
