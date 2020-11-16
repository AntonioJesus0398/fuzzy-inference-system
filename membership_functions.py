
def triangular(a1, a2, a3):
    def f(x):
        if x >= a1 and x <= a2:
            return (x - a1) / (a2 - a1)
        elif x >= a2 and x <= a3:
            return (a3 - x) / (a3 - a2)
        else:
            return 0
    return f
