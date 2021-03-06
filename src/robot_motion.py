from fis import LinguisticVariable, FuzzyRuleBase, FuzzyInferenceSystem


Angle = LinguisticVariable(name='angle', domain=(0, 180), no_levels=30)
Angle.add_term('right-large', Angle.build_rect(0, 45, 'desc'))
Angle.add_term('right-medium', Angle.build_triangular(30, 45, 60))
Angle.add_term('right-small', Angle.build_rect(45, 85, 'asc'))
Angle.add_term('zero-angle', Angle.build_singleton(90))
Angle.add_term('left-small', Angle.build_rect(95, 135, 'desc'))
Angle.add_term('left-medium', Angle.build_triangular(120, 135, 150))
Angle.add_term('left-large', Angle.build_rect(135, 180, 'asc'))

Direction = LinguisticVariable(name='direction', domain=(0, 180), no_levels=30)
Direction.add_term('right-sharp', Direction.build_rect(0, 45, 'desc'))
Direction.add_term('right-medium', Direction.build_triangular(30, 45, 60))
Direction.add_term('right-mild', Direction.build_rect(45, 85, 'asc'))
Direction.add_term('zero-turn', Direction.build_singleton(90))
Direction.add_term('left-mild', Direction.build_rect(95, 135, 'desc'))
Direction.add_term('left-medium', Direction.build_triangular(120, 135, 150))
Direction.add_term('left-sharp', Direction.build_rect(135, 180, 'asc'))

Distance = LinguisticVariable(name='distance', domain=(0, 100), no_levels=20)
Distance.add_term('pretty-near', Distance.build_rect(0 , 15, 'desc'))
Distance.add_term('near', Distance.build_triangular(0, 15, 30))
Distance.add_term('little-far', Distance.build_triangular(15, 30, 45))
Distance.add_term('far', Distance.build_triangular(30, 45, 60))
Distance.add_term('pretty-far', Distance.build_rect(45, 100, 'asc'))

# uncomment this lines to plot the variables
# Distance.plot()
# Angle.plot()
# Direction.plot()

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
    ('near', 'left-large'): 'right-mild',
    ('near', 'right-large'): 'left-mild',
    ('pretty-near', 'right-large'): 'left-medium',
    ('pretty-near', 'left-large'): 'right-medium',
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

FIS = FuzzyInferenceSystem(rule_base)
