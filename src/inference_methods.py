from src.classes import MembershipValue, FuzzySet, FuzzyRule, FuzzyRuleBase, LinguisticVariable

def mamdani(input_value, rule_base: FuzzyRuleBase):
    rules = rule_base.rules
    results = {}
    for control_variable in rules:
        def f(w):
            result = MembershipValue(0)
            for r in rules[control_variable]:
                matching_degree = MembershipValue(1)
                for i, (variable, term_name) in enumerate(r.antecedent):
                    fuzzy_set = variable.terms[term_name]
                    matching_degree &= fuzzy_set.membership_function(input_value[i])
                variable, term_name = r.consequence[0]
                result |= (matching_degree & variable.terms[term_name].membership_function(w))
            return result
        results[control_variable] = FuzzySet(f)
    return results

def larsen(input_value, rule_base: FuzzyRuleBase):
    rules = rule_base.rules
    results = {}
    for control_variable in rules:
        def f(w):
            result = MembershipValue(0)
            for r in rules[control_variable]:
                matching_degree = MembershipValue(1)
                for i, (variable, term_name) in enumerate(r.antecedent):
                    fuzzy_set = variable.terms[term_name]
                    matching_degree &= fuzzy_set.membership_function(input_value[i])
                variable, term_name = r.consequence[0]
                result |= (matching_degree * variable.terms[term_name].membership_function(w))
            return result
        results[control_variable] = FuzzySet(f)
    return results
