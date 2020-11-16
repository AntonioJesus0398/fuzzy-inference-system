INF = 1000000000000

class LinguisticVariable:
    # terms: a list of fuzzy sets
    def __init__(self, name, domain, terms):
        self.name = name
        self.domain = domain
        self.terms = terms

class FuzzySet:

    def __init__(self, name, membership_function):
        self.name = name
        self.membership_function = membership_function


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

class FuzzyRule:

    # if x is Ai and y is Bi then z is Ci
    # A, B and C are Linguistic Variables. Ai, Bi, Ci are terms of A, B, C
    def __init__(self, antecedent, consecuence):
        self.antecedent = antecedent
        self.consequence = consecuence
