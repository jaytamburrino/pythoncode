import math
import matplotlib.pyplot as plt
import numpy as np


def factorBinomial(a, b, c):
    return [(-b + math.sqrt(b ** 2 - 4 * a * c)) / (2 * a), (-b - math.sqrt(b ** 2 - 4 * a * c)) / (2 * a)]


# location and size should be defined better
def detector(dirx, diry, dirz):
    if dirx > 0:
        return 1
    else:
        return 0


# theta: rotation in xy plane, phi: rotation off of xy plane, psy: counter-clockwise rotation in shifted plane
# a: x to y width ratio, c: y to z width ratio, b= y width =1
def lightray(y, z, theta, phi, psy, a, c):
    # determines correct location of reflection
    # light assumed to come from +x direction parallel to xy plane
    # y,z coordinates known, factors to find x
    try:
        roots = factorBinomial(
            (math.cos(theta) * math.cos(phi) * math.cos(psy) - math.sin(theta) * math.sin(psy)) ** 2 / a ** 2 + (
                    math.cos(theta) * math.cos(phi) * math.sin(psy) + math.sin(theta) * math.cos(psy)) ** 2 + (
                    math.cos(theta) * math.sin(phi)) ** 2 / c ** 2,

            2 * ((math.cos(theta) * math.cos(phi) * math.cos(psy) - math.sin(theta) * math.sin(psy)) * (
                    -y * math.sin(theta) * math.cos(phi) * math.cos(psy) - y * math.cos(theta) * math.sin(
                psy) + z * math.sin(theta) * math.cos(psy)) / a ** 2 +
                 (math.cos(theta) * math.cos(phi) * math.sin(psy) + math.sin(theta) * math.cos(psy)) * (
                         -y * math.sin(theta) * math.cos(phi) * math.sin(psy) + y * math.cos(theta) * math.cos(
                     psy) + z * math.sin(theta) * math.sin(psy)) +
                 (math.cos(theta) * math.sin(phi)) * (
                             y * math.sin(theta) * math.sin(phi) - z * math.cos(phi))) / c ** 2,

            (-y * math.sin(theta) * math.cos(phi) * math.cos(psy) - y * math.cos(theta) * math.sin(psy) + z * math.sin(
                phi) * math.cos(psy)) ** 2 / a ** 2 +
            (-y * math.sin(theta) * math.cos(phi) * math.sin(psy) + y * math.cos(theta) * math.cos(psy) + z * math.sin(
                phi) * math.sin(psy)) ** 2 +
            (y * math.sin(theta) * math.sin(phi) + z * math.cos(phi)) ** 2 / c ** 2 - 1
        )
    except:
        roots = ['na', 'na']

    # find gradient of asteroid at (x,y,z)
    if roots[0] != 'na':
        if roots[0] > roots[1]:
            x = roots[0]
        else:
            x = roots[1]

        gradx = 2 * (((x * math.cos(theta) - y * math.sin(theta)) * math.cos(phi) + z * math.sin(phi)) * math.cos(
            psy) - (x * math.sin(theta) + y * math.cos(theta)) * math.sin(psy)) * (
                        math.cos(theta) * math.cos(phi) * math.cos(psy) - math.sin(theta) * math.sin(
                    psy)) / a ** 2 + 2 * (((x * math.cos(theta) - y * math.sin(theta)) * math.cos(phi) + z * math.sin(
            phi)) * math.sin(psy) + (x * math.sin(theta) + y * math.cos(theta)) * math.cos(psy)) * (
                        math.cos(theta) * math.cos(phi) * math.sin(psy) + math.sin(theta) * math.cos(psy)) \
                + 2 * (-(x * math.cos(theta) - y * math.sin(theta)) * math.sin(phi) + z * math.cos(phi)) * -math.cos(
            theta) * math.sin(phi) / c ** 2

        grady = 2 * (((x * math.cos(theta) - y * math.sin(theta)) * math.cos(phi) + z * math.sin(phi)) * math.cos(
            psy) - (x * math.sin(theta) + y * math.cos(theta)) * math.sin(psy)) * (
                        -math.sin(theta) * math.cos(phi) * math.cos(psy) - math.cos(theta) * math.sin(
                    psy)) / a ** 2 + 2 * (((x * math.cos(theta) - y * math.sin(theta)) * math.cos(phi) + z * math.sin(
            phi)) * math.sin(psy) + (x * math.sin(theta) + y * math.cos(theta)) * math.cos(psy)) * (
                        -math.sin(theta) * math.cos(phi) * math.sin(psy) + math.cos(theta) * math.cos(psy)) \
                + 2 * (-(x * math.cos(theta) - y * math.sin(theta)) * math.sin(phi) + z * math.cos(phi)) * math.sin(
            theta) * math.sin(phi) / c ** 2

        gradz = 2 * (((x * math.cos(theta) - y * math.sin(theta)) * math.cos(phi) + z * math.sin(phi)) * math.cos(
            psy) - (x * math.sin(theta) + y * math.cos(theta)) * math.sin(psy)) * math.sin(phi) * math.cos(
            psy) / a ** 2 + 2 * (((x * math.cos(theta) - y * math.sin(theta)) * math.cos(phi) + z * math.sin(
            phi)) * math.sin(psy) + (x * math.sin(theta) + y * math.cos(theta)) * math.cos(psy)) * math.sin(
            phi) * math.sin(psy) \
                + 2 * (-(x * math.cos(theta) - y * math.sin(theta)) * math.sin(phi) + z * math.cos(phi)) * math.cos(
            phi) / c ** 2

        mag = math.sqrt(gradx ** 2 + grady ** 2 + gradz ** 2)

        # outgoing light vector r, incoming vector d, normal vector n, r=d-2(d*n)n
        rx = -1 + 2 * (gradx / mag) ** 2
        ry = 2 * gradx * grady / mag ** 2
        rz = 2 * gradx * gradz / mag ** 2

        return detector(rx, ry, rz)

    else:
        return 0


# parameters
a = 2  # x:y width ratio
c = 1  # z:y width ratio
t = np.linspace(0, 360, 37)  # define theta,phi,psy as a function of time (all in radians)
def theta(t): return 0
def phi(t): return 0
def psy(t): return t * math.pi / 180
number = 101  # odd gives slightly better plotting, 100-250 usually works

# plotting for light curve
hitlist = []
for k in t:
    hits = 0
    for i in np.linspace(-a, a, number):
        for j in np.linspace(-a, a, number):
            hits += lightray(i, j, theta(k), phi(k), psy(k), a, c)
    print(k, hits)
    hitlist.append(hits)

plt.plot(t, hitlist)
plt.xlabel("Time")
plt.ylabel("Count")
plt.ylim(0, number ** 2)
plt.show()
