class LinguisticVariable:

    def __init__(self, name, levels, terms):
        self.name = name
        self.levels = levels
        self.terms = terms

class FuzzySet:

    def __init__(self, membership_function):
        self.membership_function = membership_function