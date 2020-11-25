import matplotlib.pyplot as plt
from numpy import arange

def plot(functions, interval, step=0.01):
    x = arange(interval[0],interval[1],step)
    for f, lab in functions:
        y = [f(i) for i in x]
        plt.plot(x, y, label=lab)
    plt.show()

from membership_functions import triangular

f1 = lambda x: triangular(0, 1, 2)(x).value
f2 = lambda x: triangular(0.5, 2.8, 3.1)(x).value
plot([(f1, 'f1'), (f2, 'f2')], (0, 5))
