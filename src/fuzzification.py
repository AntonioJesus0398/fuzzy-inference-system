# from src.membership_functions import triangular, singleton
# from src.classes import LinguisticVariable, FuzzySet
from membership_functions import triangular, singleton
from classes import LinguisticVariable, FuzzySet

def singleton_fuzzification(lv, x):
    return FuzzySet(membership_function=singleton(x), domain=lv.domain)
