from src.membership_functions import triangular, trapezoidal, singleton
from numpy import arange
import matplotlib.pyplot as plt

class FuzzySet:

    def __init__(self, membership_function, domain):
        self.domain = domain
        self.membership_function = membership_function


class LinguisticVariable:
    # terms: a list of fuzzy sets
    def __init__(self, name, domain, no_levels, scaling_function=lambda v: v, unscaling_function=lambda v: v):
        self.name = name
        self.domain = scaling_function(domain[0]), scaling_function(domain[1])
        self.scaling_function = scaling_function
        self.unscaling_function = unscaling_function
        self.step_size = (scaling_function(domain[1]) - scaling_function(domain[0])) / no_levels
        self.terms = {}

    def build_singleton(self, v):
        return FuzzySet(membership_function=singleton(self.scaling_function(v), step=self.step_size), domain=self.domain)

    def build_triangular(self, a1, a2, a3):
        return FuzzySet(membership_function=triangular(self.scaling_function(a1), self.scaling_function(a2), self.scaling_function(a3)), domain=self.domain)

    def build_trapezoidal(self, a1, a2, a3, a4):
        return FuzzySet(membership_function=trapezoidal(self.scaling_function(a1), self.scaling_function(a2), self.scaling_function(a3), self.scaling_function(a4)), domain=self.domain)

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
