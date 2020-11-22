from src.classes import LinguisticVariable, FuzzyRuleBase
from src.membership_functions import triangular, trapezoidal
from src.fuzzy_inference_system import FuzzyInferenceSystem

Angle = LinguisticVariable(name='angle', domain=(0, 180), no_levels=180, scaling_function=lambda v: v/180)
Angle.add_term('right-large', Angle.build_triangular(-1, 0, 45))
Angle.add_term('right-medium', Angle.build_triangular(30, 45, 60))
Angle.add_term('right-small', Angle.build_triangular(45, 67.5, 90))
Angle.add_term('zero-angle', Angle.build_singleton(90))
Angle.add_term('left-small', Angle.build_triangular(90, 112.5, 135))
Angle.add_term('left-medium', Angle.build_triangular(120, 135, 150))
Angle.add_term('left-large', Angle.build_triangular(135, 180, 181))

Direction = LinguisticVariable(name='direction', domain=(0, 180), scaling_function=lambda v: v/180, unscaling_function=lambda v: v * 180, no_levels=180)
Direction.add_term('right-sharp', Direction.build_triangular(-1, 0, 45))
Direction.add_term('right-medium', Direction.build_triangular(30, 45, 60))
Direction.add_term('right-mild', Direction.build_triangular(45, 67.5, 90))
Direction.add_term('zero-turn', Direction.build_singleton(90,))
Direction.add_term('left-mild', Direction.build_triangular(90, 112.5, 135))
Direction.add_term('left-medium', Direction.build_triangular(120, 135, 150))
Direction.add_term('left-sharp', Direction.build_triangular(135, 180, 181))

Distance = LinguisticVariable(name='distance', domain=(0, 100), scaling_function=lambda v: v / 100, no_levels=100)
Distance.add_term('pretty-near', Distance.build_triangular(-1, 0 , 15))
Distance.add_term('near', Distance.build_triangular(0, 15, 30))
Distance.add_term('little-far', Distance.build_triangular(15, 30, 45))
Distance.add_term('far', Distance.build_triangular(30, 45, 60))
Distance.add_term('pretty-far', Distance.build_triangular(45, 100, 101))

rule_base = FuzzyRuleBase(state_variables=[Distance, Angle], control_variables=[Direction])

space_partition = {
    ('far', 'right-small'): 'left-mild',
    ('far', 'zero-angle'): 'right-mild',
    ('far', 'left-small'): 'right-mild',
    ('little-far', 'right-medium'): 'left-mild',
    ('little-far', 'right-small'): 'left-medium',
    ('little-far', 'zero-angle'): 'right-medium',
    ('little-far', 'left-small'): 'right-medium',
    ('little-far', 'left-medium'): 'right-mild',
    ('near', 'right-medium'): 'left-mild',
    ('near', 'right-small'): 'left-sharp',
    ('near', 'zero-angle'): 'right-sharp',
    ('near', 'left-small'): 'right-sharp',
    ('near', 'left-medium'): 'right-mild',
    ('pretty-near', 'right-medium'): 'left-medium',
    ('pretty-near', 'right-small'): 'left-sharp',
    ('pretty-near', 'zero-angle'): 'right-sharp',
    ('pretty-near', 'left-small'): 'right-sharp',
    ('pretty-near', 'left-medium'): 'right-medium'
}

for d_term in Distance.terms:
    for a_term in Angle.terms:
        try:
            rule_base.add_rule([('distance', d_term), ('angle', a_term)], [('direction', space_partition[d_term, a_term])])
        except KeyError:
            rule_base.add_rule([('distance', d_term), ('angle', a_term)], [('direction', 'zero-turn')])

for control_variable in rule_base.rules:
    for rule in rule_base.rules[control_variable]:
        print(rule)

FIS = FuzzyInferenceSystem(rule_base, inference_method="Larsen")

a = FIS.solve([('distance', Distance.build_singleton(8)), ('angle', Angle.build_singleton(88))])
# print(a)
