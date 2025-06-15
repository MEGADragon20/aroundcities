import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import fsolve

# Gegebene Werte
G = 6.674 * 10**-11  # Gravitationskonstante in N*m^2/kg^2
m1 = 5.972 * 10**24  # Masse der Erde in kg
m2 = 7.348 * 10**22  # Masse des Mondes in kg
a = 384400000  # große Halbachse in Metern (Abstand Erde-Mond)
e = 0.0549  # Exzentrizität der Mondbahn
T = 27 * 24 * 3600  # Umlaufzeit in Sekunden (ca. 27.3 Tage)
n = 2 * np.pi / T  # mittlere Bewegung

# Berechnung der reduzierten Gravitationskonstanten (mu)
mu = G * (m1 + m2)

# Funktion zur Berechnung der mittleren Anomalie M(t)
def M(t):
    return n * t

# Funktion zur Berechnung der Keplerschen Gleichung: M(t) = E(t) - e * sin(E(t))
def kepler_eq(E, M):
    return E - e * np.sin(E) - M

# Numerische Lösung der Keplerschen Gleichung für E(t)
def solve_kepler(M):
    E_initial_guess = M  # Annahme: Anfangsschätzwert ist M
    E_solution = fsolve(kepler_eq, E_initial_guess, args=(M))
    return E_solution[0]

# Berechnung der wahren Anomalie theta(t) aus E(t)
def true_anomaly(E):
    return 2 * np.arctan(np.sqrt((1 + e) / (1 - e)) * np.tan(E / 2))

# Berechnung des Abstands r(t)
def distance(t):
    M_t = M(t)  # Mittlere Anomalie
    E_t = solve_kepler(M_t)  # Lösung der Keplerschen Gleichung
    theta_t = true_anomaly(E_t)  # Wahre Anomalie
    r_t = a * (1 - e**2) / (1 + e * np.cos(theta_t))  # Abstand r(t)
    return r_t

# Berechnung der Geschwindigkeit v(t)
def velocity(t):
    r_t = distance(t)  # Berechnung des Abstands r(t)
    M_t = M(t)  # Mittlere Anomalie
    E_t = solve_kepler(M_t)  # Lösung der Keplerschen Gleichung
    v_t = np.sqrt(mu * (2 / r_t - 1 / a))  # Geschwindigkeit v(t)
    return v_t

t_ = []
v_ = []
r_ = []
for i in range(3*31*24):  # Zeit in Stunden
    t = i * 3600 # Zeit in Stunden
    print(t)
    v_t = velocity(t)
    r_t = distance(t)  # Berechnung des Abstands r(t)
    t_.append(t)
    r_.append(r_t/1000)
    v_.append(v_t)

f, (a, b) = plt.subplots(2, 1)
a.plot(t_, v_, label='Geschwindigkeit v(t)')
b.plot(t_, r_, label='Abstand r(t)')
a.set_xlabel('Zeit (s)')
a.set_ylabel('Geschwindigkeit (m/s)')
b.set_xlabel('Zeit (s)')
b.set_ylabel('Abstand (km)')
a.legend()
b.legend()


plt.show()