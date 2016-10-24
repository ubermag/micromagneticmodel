import math

# Fundamental constants
mu0 = 4 * math.pi * 1e-7  # magnetic constant (N/A**2)
e = 1.6021766208e-19  # elementary charge (C)
me = 9.1093835611e-31  # electron mass (kg)
kB = 1.3806485279e-23  # Boltzmann constant (J/K)
h = 6.62607004081e-34  # Planck constant (Js)
g = 2.00231930436182  # Lande g-factor

# Derived constants
hbar = h/(2*math.pi)  # reduced Planck constant (Js)
gamma = g*e/(2*me)  # gyrotropic ratio (C/kg)
muB = gamma*hbar  # Bohr magneton (J/T)
gamma0 = gamma*mu0  # LLG precession term gamma (m/As)
