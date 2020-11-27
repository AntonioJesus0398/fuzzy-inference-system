import unittest
from src.inference_methods import aggregate
from src.membership_functions import triangular, trapezoidal, singleton
from src.classes import FuzzySet, FuzzyRule, FuzzyRuleBase, LinguisticVariable

A = LinguisticVariable('A', domain=(0, 1), no_levels=1000)
A.add_term('A1', A.build_triangular(0, 0.5, 1))
A.add_term('A2', A.build_singleton(0.35))

B = LinguisticVariable('B', domain=(0, 1), no_levels=1000)
B.add_term('B1', B.build_triangular(0.2, 0.4, 0.9))
B.add_term('B2', B.build_triangular(0.1, 0.3, 0.6))

C = LinguisticVariable('C', domain=(0, 1), no_levels=1000)
C.add_term('C1', B.build_trapezoidal(0.1, 0.2, 0.5, 1))
C.add_term('C2', B.build_triangular(0, 0.2, 0.4))

D = LinguisticVariable('D', domain=(0, 1), no_levels=1000)
D.add_term('D1', D.build_singleton(0.4))
D.add_term('D2', D.build_triangular(0.1, 0.3, 0.8))

RB = FuzzyRuleBase((A, B), (C, D))
RB.add_rule([('A', 'A1'), ('B', 'B1')], [('C', 'C1'), ('D', 'D1')])
RB.add_rule([('A', 'A2'), ('B', 'B2')], [('C', 'C2'), ('D', 'D2')])

class InferenceMethodsTestCase(unittest.TestCase):
    def test_mamdani_singleton_input(self):
        # _input = [('A', A.build_singleton(0.3)), ('B', B.build_singleton(0.8))]
        # result = aggregate(_input, RB)
        # f = result['C'].membership_function

        f = A.terms['A2'].membership_function
        x = 0
        while x < 1: 
            print(x, f(x).value)
            x += A.step_size
        # self.assertAlmostEqual(f(0.1).value, 0, 1)
        # self.assertAlmostEqual(f(0.2).value, 0.2, 1)
        # self.assertAlmostEqual(f(0.21).value, 0.2, 1)
        # self.assertAlmostEqual(f(1).value, 0, 1)
        # self.assertAlmostEqual(f(0.15).value, 0.2, 1)
        # self.assertAlmostEqual(f(0.95).value, 0.1, 1)

    # def test_larsen_singleton_input(self):
    #     _input = [('A', A.build_singleton(0.3)), ('B', B.build_singleton(0.8))]
    #     result = aggregate(_input, RB, method="Larsen")
    #     f = result['C'].membership_function

    #     _t = C.discretize(0.2)
    #     print(_t)
    #     # self.assertAlmostEqual(f(0.1).value, 0, 1)
    #     self.assertAlmostEqual(f(_t).value, _t, 2)
    #     # self.assertAlmostEqual(f(0.21).value, 0.2, 1)
    #     # self.assertAlmostEqual(f(1).value, 0, 1)
    #     # self.assertAlmostEqual(f(0.15).value, 0.1, 1)
    #     # self.assertAlmostEqual(f(0.95).value, 0.02, 2)

    # def test_mamdani_fuzzy_input(self):
    #     _input = [('A', A.build_triangular(0.1, 0.7, 0.8)), ('B', B.build_trapezoidal(0, 0.3, 0.5, 0.8))]
    #     result = aggregate(_input, RB)
    #     f = result['C'].membership_function
    #     self.assertAlmostEqual(f(0.3).value, 0.82, 2)
    #     self.assertAlmostEqual(f(0.6).value, 0.8, 1)

    # def test_larsen_fuzzy_input(self):
    #     _input = [('A', A.build_triangular(0.1, 0.7, 0.8)), ('B', B.build_trapezoidal(0, 0.3, 0.5, 0.8))]
    #     result = aggregate(_input, RB, method="Larsen")
    #     f = result['C'].membership_function
    #     self.assertAlmostEqual(f(0.3).value, 0.82, 2)
    #     self.assertAlmostEqual(f(0.6).value, 0.65, 2)
