from src.classes import MembershipValue, FuzzySet, FuzzyRule, FuzzyRuleBase, LinguisticVariable

def aggregate(input_value, rule_base: FuzzyRuleBase, method="Mamdani", step=0.01):
    if method not in ["Mamdani", "Larsen"]:
        raise ValueError("Invalid aggregation method")
    rules = rule_base.rules
    results = {}
    for control_variable in rules:
        def f(w):
            result = MembershipValue(0)
            for r in rules[control_variable]:
                matching_degree = get_matching_degree(zip(input_value, [variable.terms[term_name] for variable, term_name in r.antecedent]), step)
                variable, term_name = r.consequence[0]
                if method == "Mamdani":
                    result |= (matching_degree & variable.terms[term_name].membership_function(w))
                else:
                    result |= (matching_degree * variable.terms[term_name].membership_function(w))
            return result
        results[control_variable] = FuzzySet(f, domain=rule_base.control_variables[control_variable].domain)
    return results

def get_matching_degree(fuzzy_sets, step):
    matching_degree = MembershipValue(1)
    for fuzzy_sets_pair in fuzzy_sets:
        A, B = fuzzy_sets_pair
        left, right = min(A.domain[0], B.domain[0]), max(A.domain[1], B.domain[1])
        x = left
        _max = MembershipValue(0)
        while x <= right:
            _max |= A.membership_function(x) & B.membership_function(x)
            x += step
        matching_degree &= _max
    return matching_degree
