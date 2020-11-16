INF = 1000000000000

class LinguisticVariable:

    def __init__(self, name, domain, terms):
        self.name = name
        self.domain = domain
        self.terms = terms

class FuzzySet:

    def __init__(self, name, membership_function):
        self.name = name
        self.membership_function = membership_function