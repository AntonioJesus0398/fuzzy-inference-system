from robot_motion import FIS, Distance, Angle
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
RIGHT = 60
START = 25
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
        write(f"Position: {round(robot.center.x, 2), round(robot.center.y, 2)} ")
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
        write(f"Nearest: {round(shortest_distance, 2), round(angle, 1)} ")
        # Compute the new direction to take and move in that direction
        try:
            new_direction_angle = FIS.solve([('distance', Distance.build_singleton(shortest_distance)), ('angle', Angle.build_singleton(angle))], inference_method=inference_method, defuzzification_method=defuzzification_method)['direction']
        except ZeroDivisionError:
            print(shortest_distance, angle)
            exit(1)
        write(f"direction: {new_direction_angle}\n")
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
        radius=random.randint(2, 5)
        write(f"({x}, {y}): {radius}\n")
        c = Circle(center=Point(x, y), radius=radius)
        obstacles.append(c)
    write('\n\n')
    return obstacles


def perform_simulations(no_simulations):
    inference_methods = ["Mamdani", "Larsen"]
    defuzzification_methods = ["coa", "boa"]
    results = {(im, dm): 0 for im in inference_methods for dm in defuzzification_methods}

    for i in range(no_simulations):
        print(f"Simulation #{i}\n")
        write(f"\n\n--------------------------Simulation #{i}-------------------\n\n")
        start_point = Point(LEFT + RIGHT / 2, 0)
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
