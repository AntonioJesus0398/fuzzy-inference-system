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

class MembershipDegree:

    def __init__(self, value):
        self.value = value

    def __and__(self, other):
        return MembershipDegree(min(self.value, other.value))

    def __or__(self, other):
        return MembershipDegree(max(self.value, other.value))

    def __repr__(self):
        return str(self.value)
