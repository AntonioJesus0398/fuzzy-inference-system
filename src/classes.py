from src.membership_functions import triangular, trapezoidal, singleton, rect
from numpy import arange
import matplotlib.pyplot as plt

class FuzzySet:

    def __init__(self, membership_function, domain):
        self.domain = domain
        self.membership_function = membership_function


class LinguisticVariable:
    # terms: a list of fuzzy sets
    def __init__(self, name, domain, no_levels):
        self.name = name
        self.domain = domain
        self.step_size = (domain[1] - domain[0]) / no_levels
        self.terms = {}

    def discretize(self, value):
        left, right = self.domain
        if value < left or value > right:
            return value

        x = left
        previous = left
        while x < value:
            previous = x
            x += self.step_size

        d1 = abs(value - x)
        d2 = abs(value - previous)

        if d1 < d2:
            return x
        return previous

    def build_singleton(self, v):
        return FuzzySet(membership_function=singleton(self.discretize(v)), domain=self.domain)

    def build_triangular(self, a1, a2, a3):
        return FuzzySet(membership_function=triangular(self.discretize(a1), self.discretize(a2), self.discretize(a3)), domain=self.domain)

    def build_rect(self, a1, a2, monotony):
        return FuzzySet(membership_function=rect(self.discretize(a1), self.discretize(a2), monotony=monotony), domain=self.domain)

    def build_trapezoidal(self, a1, a2, a3, a4):
        return FuzzySet(membership_function=trapezoidal(self.discretize(a1), self.discretize(a2), self.discretize(a3), self.discretize(a4)), domain=self.domain)

    
    def add_term(self, name, fz):
        self.terms[name] = fz

    def plot(self):
        x = arange(self.domain[0], self.domain[1], self.step_size)
        for term_name, fz in self.terms.items():
            y = [fz.membership_function(i).value for i in x]
            plt.plot(x, y, label=term_name)
        plt.legend(loc='best', fontsize="small")
        plt.show()

    def __eq__(self, other):
        return self.name == other.name


class FuzzyRule:

    # if x1 is A1 and x2 is A2 and ... and xn is An then y1 is B1 and 2y is B2 and ... ym is Bm
    def __init__(self, antecedent: [LinguisticVariable, str], consequence: [LinguisticVariable, str]):
        self.antecedent = antecedent
        self.consequence = consequence

    def __repr__(self):
        premise = [f' {lv.name} is {term} ' for lv, term in self.antecedent]
        conclusion = [f' {lv.name} is {term} ' for lv, term in self.consequence]
        return 'If' + 'and'.join(premise) + 'then' + 'and'.join(conclusion)


class FuzzyRuleBase:
    def __init__(self, state_variables, control_variables):
        self.rules = {}
        self.state_variables = {sv.name: sv for sv in state_variables}
        self.control_variables = {cv.name: cv for cv in control_variables}

    def __iter__(self):
        return iter(self.rules)

    def add_rule(self, _antecedent, _consequence):
        antecedent = [(self.state_variables[variable_name], term_name) for variable_name, term_name in _antecedent]
        consequence = [(self.control_variables[variable_name], term_name) for variable_name, term_name in _consequence]
        for variable, term_name in consequence:
            try:
                self.rules[variable.name].append(FuzzyRule(antecedent, [(variable, term_name)]))
            except KeyError:
                self.rules[variable.name] = [FuzzyRule(antecedent, [(variable, term_name)])]
