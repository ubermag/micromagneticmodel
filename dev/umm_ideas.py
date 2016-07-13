from micromagneticmodel.energies import Zeeman


class MicromagneticModel(object):
    def __init__(self, cmin, cmax, d, Ms, name):
        self.cmin = cmin
        self.cmax = cmax
        self.d = d
        self.Ms = Ms
        self.name = name

        self.alpha = 1
        
        self.energies = []
        self.llg_terms = []

    def __str__(self):
        return "AbstractMicromagneticModell(name={})".format(self.name)

    def add(self, energy):
        energies.append(energy)

    def set_H(self, H):
        print("AbstractMicromagneticModell: setting field = {}")
        for energy in self.energies:
            if isinstance(energy, Zeeman):
                self.energies.remove(energy)
        self.add(Zeeman(H))

    def set_m(self, m0):
        self.m0 = m0
        
    def relax(self):
        raise NotImplementedError("relax is abstract method")

    def m_average(self):
        raise NotImplementedError("m_average is abstract method")

    def total_energy(self):
        raise NotImplementedError("total_energy is abstract method")
    
    def hysteresis(self, fieldlist):
        print("AbstractMicromagneticModell: starting hysteresis")
        for field in fieldlist:
            self.set_H(field)
            self._relax()


class OOMMFC(AbstractMicromagneticModell):

    def __init__(self, name, Ms):
        AbstractMicromagneticModell.__init__(self, name, Ms)

    def __str__(self):
        return "OOMMFC(name={}, Ms={})".format(self.name, self.Ms)

    def _relax(self):
        print("Calling OOMMF to run relax() with H={}".format(self.field))

class FIDIMAGC(AbstractMicromagneticModell):

    def __init__(self, name, Ms):
        AbstractMicromagneticModell.__init__(self, name, Ms)

    def __str__(self):
        return "FIDIMAG(name={}, Ms={})".format(self.name, self.Ms)

    def _relax(self):
        print("Calling FIDIMAG to run relax() with H={}".format(self.field))


#a = AbstractMicromagneticModell('simulation-name', 10)

#print(a)
#a.hysteresis([10, 20])

o = OOMMFC(name='oommf-simulation', Ms=8e6)
print(o)
o.relax()

f = FIDIMAGC(name='fidimag-simulation', Ms=8e6)
print(o)
f.relax()

#o.relax()
#o.hysteresis([10, 20, 30])
