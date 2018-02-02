"""
MAT 3570: Lab 1
Submitted by: Jay Tamburrino
"""

import scipy as sp
import matplotlib.pyplot as plt
import math


def horner(coeff):
    def f(x):
        result=0
        xpow=1
        for a in coeff:
            result += a*xpow
            xpow*=x
        return result
    return f


def plotPoly(coeff, left, right, numPoints):
    X = sp.linspace(left, right, numPoints, endpoint=True)
    Y = horner(coeff)
    plt.plot(X, Y(X), X,(X-1)**6)
    plt.show()


plotPoly([1,-6,15,-20,15,-6,1], -1, 3, 100)
plotPoly([1,-6,15,-20,15,-6,1], .995, 1.005, 100)


def r1(l):
    if len(l) !=3:
        return None
    return (-l[1]+math.sqrt(l[1]**2-4*l[0]*l[2]))/(2*l[2])

def r2(l):
    if len(l) !=3:
        return None
    return (-l[1]-math.sqrt(l[1]**2-4*l[0]*l[2]))/(2*l[2])


s=[3,4,1]
print(r1(s), r2(s))

s=[-3,9**12,1]
print(r1(s), r2(s))


g=horner(s)
print(g(r1(s)),g(r2(s)))