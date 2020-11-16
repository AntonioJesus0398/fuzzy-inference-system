
def triangular(a1, a2, a3):
    def f(x):
        if x >= a1 and x <= a2:
            return (x - a1) / (a2 - a1)
        if x >= a2 and x <= a3:
            return (a3 - x) / (a3 - a2)
        return 0
    return f

def trapezoidal(a1, a2, a3, a4):
    def f(x):
        if x >= a1 and x <= a2:
            return (x - a1) / (a2 - a1)
        if x >= a2 and x <= a3:
            return 1
        if x >= a3 and x <= a4:
            return (a4 - x) / (a4 - a3)
        return 0
    return f