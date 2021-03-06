class MembershipValue:

    def __init__(self, value):
        self.value = value

    def __and__(self, other):
        return MembershipValue(min(self.value, other.value))

    def __or__(self, other):
        return MembershipValue(max(self.value, other.value))

    def __mul__(self, other):
        return MembershipValue(self.value * other.value)

    def __repr__(self):
        return str(self.value)


def membership_function(f):
    def func(*args):
        return MembershipValue(f(*args))
    return func

def triangular(a1, a2, a3):
    @membership_function
    def f(x):
        # print(x, a1, a2, a3)
        if x >= a1 and x <= a2:
            return (x - a1) / (a2 - a1)
        if x >= a2 and x <= a3:
            return (a3 - x) / (a3 - a2)
        return 0
    return f

def rect(a1, a2, monotony='asc'):
    @membership_function
    def f(x):
        if monotony == 'asc' and x >= a1 and x <= a2:
            return (x - a1) / (a2 - a1)
        if monotony == 'desc' and x >= a1 and x <= a2:
            return (a2 - x) / (a2 - a1)
        return 0
    return f

def trapezoidal(a1, a2, a3, a4):
    @membership_function
    def f(x):
        if x >= a1 and x <= a2:
            return (x - a1) / (a2 - a1)
        if x >= a2 and x <= a3:
            return 1
        if x >= a3 and x <= a4:
            return (a4 - x) / (a4 - a3)
        return 0
    return f

def singleton(value):
    @membership_function
    def f(x):
        if x == value:
            return 1
        return 0
    return f
