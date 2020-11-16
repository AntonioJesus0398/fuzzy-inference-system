from classes import MembershipValue, FuzzySet, FuzzyRule, LinguisticVariable

def mamdani(input_value, rules):
    u, v = input_value

    def f(w):
        result = MembershipValue(0)
        for r in rules:
            (A, B), C = r.antecedent, r.consequence
            matching_degree = A.membership_function(u) & B.membership_function(v)
            result |= (matching_degree & C.membership_function(w))
        return result

    return FuzzySet('', f)

def larsen(input_value, rules):
    u, v = input_value

    def f(w):
        result = MembershipValue(0)
        for r in rules:
            (A, B), C = r.antecedent, r.consequence
            matching_degree = A.membership_function(u) & B.membership_function(v)
            result |= (matching_degree * C.membership_function(w))
        return result

    return FuzzySet('', f)
