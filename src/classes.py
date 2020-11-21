# from src.fuzzification import scale_function


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

    def add_term(self, name, func, args):
        scaled_args = tuple(self.scaling_function(arg) for arg in args)
        kwargs = {'step': self.step_size}
        self.terms[name] = FuzzySet(membership_function=func(*scaled_args, **kwargs), domain=self.domain)

    def build_set(self, func, args):
        scaled_args = tuple(self.scaling_function(arg) for arg in args)
        kwargs = {'step': self.step_size}
        return FuzzySet(membership_function=func(*scaled_args, **kwargs), domain=self.domain)

    def __eq__(self, other):
        return self.name == other.name

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
