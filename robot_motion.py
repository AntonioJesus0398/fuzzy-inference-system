from src.classes import LinguisticVariable, FuzzyRuleBase
from src.membership_functions import triangular, trapezoidal
from src.fuzzy_inference_system import FuzzyInferenceSystem


Angle = LinguisticVariable(name='angle', domain=(0, 180), no_levels=30)
Angle.add_term('right-large', Angle.build_triangular(-1, 0, 45))
Angle.add_term('right-medium', Angle.build_triangular(30, 45, 60))
Angle.add_term('right-small', Angle.build_triangular(45, 67.5, 90))
Angle.add_term('zero-angle', Angle.build_singleton(90))
Angle.add_term('left-small', Angle.build_triangular(90, 112.5, 135))
Angle.add_term('left-medium', Angle.build_triangular(120, 135, 150))
Angle.add_term('left-large', Angle.build_triangular(135, 180, 181))

Direction = LinguisticVariable(name='direction', domain=(0, 180), no_levels=30)
Direction.add_term('right-sharp', Direction.build_triangular(-1, 0, 45))
Direction.add_term('right-medium', Direction.build_triangular(30, 45, 60))
Direction.add_term('right-mild', Direction.build_triangular(45, 67.5, 90))
Direction.add_term('zero-turn', Direction.build_singleton(90,))
Direction.add_term('left-mild', Direction.build_triangular(90, 112.5, 135))
Direction.add_term('left-medium', Direction.build_triangular(120, 135, 150))
Direction.add_term('left-sharp', Direction.build_triangular(135, 180, 181))

Distance = LinguisticVariable(name='distance', domain=(0, 100), no_levels=20)
Distance.add_term('pretty-near', Distance.build_triangular(-1, 0 , 15))
Distance.add_term('near', Distance.build_triangular(0, 15, 30))
Distance.add_term('little-far', Distance.build_triangular(15, 30, 45))
Distance.add_term('far', Distance.build_triangular(30, 45, 60))
Distance.add_term('pretty-far', Distance.build_triangular(45, 100, 101))

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


# ------------------------------------------------------------------------------------------------
import math
import random

def from_sex_to_rad(_input):
    return (math.pi * _input ) / 180

def from_rad_to_sex(_input):
    return (_input * 180) / math.pi

def cos(x):
    _x = from_sex_to_rad(x)
    return math.cos(_x)

def sin(x):
    _x = from_sex_to_rad(x)
    return math.sin(_x)

def asin(x):
    _x = from_rad_to_sex(x)
    return math.asin(_x)

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def distance(self, other):
        d = math.sqrt((self.x - other.x)**2 + (self.y - other.y)**2)
        if d > 100:
            return 100
        return d

class Circle:
    def __init__(self, center, radius):
        self.center = center
        self.radius = radius

    def distance_and_angle(self, other):
        hip = self.center.distance(other.center)
        d = hip - self.radius - other.radius
        co = Point(self.center.x, self.center.y).distance(Point(other.center.x, self.center.y))
        sx = co / hip
        x = math.asin(sx)
        x = (180 * x) / math.pi
        if other.center.x < self.center.x:
            x = 180 - x
        return d, x

LEFT = 0
RIGHT = 100
START = 40
FINISH = 100
ROBOT_SIZE = 1



logger = open('logging.txt', "w")
logger.close()
def write(s):
    with open('logging.txt', "a") as logger:
        logger.write(s)

def simulate(robot, obstacles, inference_method, defuzzification_method):
    while len(obstacles) > 0:
        # Look for the nearest object to the robot
        # print(f"Position: {robot.center.x, robot.center.y}")
        # print(obstacles)
        write(f"Position: {robot.center.x, robot.center.y}\n")
        shortest_distance, angle = robot.distance_and_angle(obstacles[0])
        for o in obstacles[1:]:
            d, a = robot.distance_and_angle(o)
            if d < shortest_distance:
                shortest_distance, angle = d, a

        # the borders are also objects
        left = Circle(center=Point(LEFT, robot.center.y), radius=0)
        d, a = robot.distance_and_angle(left)
        if d < shortest_distance:
            shortest_distance, angle = d, a
        right = Circle(center=Point(RIGHT, robot.center.y), radius=0)
        d, a = robot.distance_and_angle(right)
        if d < shortest_distance:
            shortest_distance, angle = d, a

        # Compute the new direction to take and move in that direction
        try:
            new_direction_angle = FIS.solve([('distance', Distance.build_singleton(shortest_distance)), ('angle', Angle.build_singleton(angle))], inference_method=inference_method, defuzzification_method=defuzzification_method)['direction']
        except ZeroDivisionError:
            print(shortest_distance, angle)
            exit(1)
        new_position = Point(robot.center.x + cos(new_direction_angle), robot.center.y + sin(new_direction_angle))
        robot.center = new_position

        # Check if a colission has been ocurred
        for o in obstacles + [left, right]:
            if robot.distance_and_angle(o)[0] <= 0:
                
                write(f"FAIL!!!!!!!!!!!!!. Object: ({o.center.x, o.center.y}): {o.radius}\n\n\n\n")
                return "fail"

        # remove passed objects
        new_obstacles = []
        for o in obstacles:
            if o.center.y >= robot.center.y:
                new_obstacles.append(o)
        obstacles = new_obstacles

    return "success"


def set_obstacles():
    obstacles = []
    no_obstacles = 10
    write(f"Obstacles:\n")
    for _ in range (no_obstacles):
        x = random.randint(LEFT, RIGHT)
        y = random.randint(START, FINISH)
        radius=random.randint(5, 10)
        write(f"({x}, {y}): {radius}\n")
        c = Circle(center=Point(x, y), radius=radius)
        obstacles.append(c)
    write('\n\n')
    return obstacles


def perform_simulations(no_simulations):
    inference_methods = ["Mamdani", "Larsen"]
    defuzzification_methods = ["coa", "boa", "mom"]
    results = {(im, dm): 0 for im in inference_methods for dm in defuzzification_methods}

    for i in range(no_simulations):
        print(f"Simulation #{i}\n")
        write(f"\n\n--------------------------Simulation #{i}-------------------\n\n")
        start_point = Point(random.randint(LEFT + ROBOT_SIZE + 2, RIGHT - ROBOT_SIZE - 2), 0)
        obstacles = set_obstacles()
        for im in inference_methods:
            for dm in defuzzification_methods:
                write(f'{im}, {dm}\n')
                results[im, dm] = 0
                robot = Circle(center=start_point, radius=ROBOT_SIZE)
                obstacles_copy = list(obstacles)
                result = simulate(robot, obstacles_copy, inference_method=im, defuzzification_method=dm)
                if result == "fail":
                    results[im, dm] += 1
                else:
                    write('SUCCESS!!!!!!!!!\n\n\n\n')

    return results


results = perform_simulations(10)
print(results)

# class InputError(Exception):
#     pass

# while True:
#     while True:
#         distance = input("Introduzca la distancia a la que se encuentra el objeto. (Debe ser un número entre 0 y 100): ")
#         try:
#             distance = int(distance)
#             if distance < 0 or distance > 100: raise InputError()
#             break
#         except:
#             print("La distancia debe de ser un número entre 0 y 100")
#             continue

#     while True:
#         angle = input("Introduzca el ángulo que forma el objeto con el robot. (Debe ser un número entre 0 y 180): ")
#         try:
#             angle = int(angle)
#             if angle < 0 or angle > 180: raise InputError()
#             break
#         except:
#             print("El ángulo debe ser un número entre 0 y 180")
#             continue

#     result = FIS.solve([('distance', Distance.build_singleton(distance)), ('angle', Angle.build_singleton(angle))])
#     print(f"El ángulo de la dirección que debe tomar el robot es: {result['direction']}")

#     while True:
#         choice = input("Desea continuar(s/n)?: ")
#         if choice == 's':
#             print('\n')
#             break
#         if choice == 'n':
#             exit(0)
