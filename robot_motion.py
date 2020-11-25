from src.classes import LinguisticVariable, FuzzyRuleBase
from src.membership_functions import triangular, trapezoidal
from src.fuzzy_inference_system import FuzzyInferenceSystem


Angle = LinguisticVariable(name='angle', domain=(0, 180), no_levels=1800, scaling_function=lambda v: v/180)
Angle.add_term('right-large', Angle.build_triangular(-1, 0, 45))
Angle.add_term('right-medium', Angle.build_triangular(30, 45, 60))
Angle.add_term('right-small', Angle.build_triangular(45, 67.5, 90))
Angle.add_term('zero-angle', Angle.build_singleton(90))
Angle.add_term('left-small', Angle.build_triangular(90, 112.5, 135))
Angle.add_term('left-medium', Angle.build_triangular(120, 135, 150))
Angle.add_term('left-large', Angle.build_triangular(135, 180, 181))

Direction = LinguisticVariable(name='direction', domain=(0, 180), scaling_function=lambda v: v/180, unscaling_function=lambda v: v * 180, no_levels=1800)
Direction.add_term('right-sharp', Direction.build_triangular(-1, 0, 45))
Direction.add_term('right-medium', Direction.build_triangular(30, 45, 60))
Direction.add_term('right-mild', Direction.build_triangular(45, 67.5, 90))
Direction.add_term('zero-turn', Direction.build_singleton(90,))
Direction.add_term('left-mild', Direction.build_triangular(90, 112.5, 135))
Direction.add_term('left-medium', Direction.build_triangular(120, 135, 150))
Direction.add_term('left-sharp', Direction.build_triangular(135, 180, 181))

Distance = LinguisticVariable(name='distance', domain=(0, 100), scaling_function=lambda v: v / 100, no_levels=1000)
Distance.add_term('pretty-near', Distance.build_triangular(-1, 0 , 15))
Distance.add_term('near', Distance.build_triangular(0, 15, 30))
Distance.add_term('little-far', Distance.build_triangular(15, 30, 45))
Distance.add_term('far', Distance.build_triangular(30, 45, 60))
Distance.add_term('pretty-far', Distance.build_triangular(45, 100, 101))

Distance.plot()
Angle.plot()
Direction.plot()


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

FIS = FuzzyInferenceSystem(rule_base, inference_method="Larsen")

class InputError(Exception):
    pass

while True:
    while True:
        distance = input("Introduzca la distancia a la que se encuentra el objeto. (Debe ser un número entre 0 y 100): ")
        try:
            distance = int(distance)
            if distance < 0 or distance > 100: raise InputError()
            break
        except:
            print("La distancia debe de ser un número entre 0 y 100")
            continue

    while True:
        angle = input("Introduzca el ángulo que forma el objeto con el robot. (Debe ser un número entre 0 y 180): ")
        try:
            angle = int(angle)
            if angle < 0 or angle > 180: raise InputError()
            break
        except:
            print("El ángulo debe ser un número entre 0 y 180")
            continue

    result = FIS.solve([('distance', Distance.build_singleton(distance)), ('angle', Angle.build_singleton(angle))])
    print(f"El ángulo de la dirección que debe tomar el robot es: {result['direction']}")

    while True:
        choice = input("Desea continuar(s/n)?: ")
        if choice == 's':
            print('\n')
            break
        if choice == 'n':
            exit(0)
