from src.classes import FuzzySet, FuzzyRule, FuzzyRuleBase, LinguisticVariable
from src.membership_functions import MembershipValue


# from classes import FuzzySet, FuzzyRule, FuzzyRuleBase, LinguisticVariable
# from membership_functions import MembershipValue

def aggregate(input_value, rule_base: FuzzyRuleBase, method="Mamdani"):
    if method not in ["Mamdani", "Larsen"]:
        raise ValueError("Invalid aggregation method")
    rules = rule_base.rules
    results = {}
    for control_variable in rules:
        def f(w):
            result = MembershipValue(0)
            for r in rules[control_variable]:
                matching_degree = get_matching_degree(zip(input_value, [variable.terms[term_name] for variable, term_name in r.antecedent]), rule_base)
                variable, term_name = r.consequence[0]
                if method == "Mamdani":
                    result |= (matching_degree & variable.terms[term_name].membership_function(w))
                else:
                    result |= (matching_degree * variable.terms[term_name].membership_function(w))
            return result
        results[control_variable] = FuzzySet(membership_function=lambda x: f(x), domain=rule_base.control_variables[control_variable].domain)
    return results

def get_matching_degree(fuzzy_sets, rule_base):
    matching_degree = MembershipValue(1)
    for fuzzy_sets_pair in fuzzy_sets:
        (variable_name, A), B = fuzzy_sets_pair
        variable = rule_base.state_variables[variable_name]
        left, right = variable.domain
        x = left
        _max = MembershipValue(0)
        while x <= right:
            _max |= (A.membership_function(x) & B.membership_function(x))
            x += variable.step_size
        matching_degree &= _max
    return matching_degree
