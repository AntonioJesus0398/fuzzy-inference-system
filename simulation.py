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

    def distance_to_point(self, other):
        d = math.sqrt((self.x - other.x)**2 + (self.y - other.y)**2)
        co = (abs(self.y - other.y))
        sx = co / d
        x = math.asin(sx)
        x = (180 * x) / math.pi
        if other.x < self.x:
            x = 180 - x
        if d > 100:
            d = 100
        return d, x

    def is_inside_of(self, rectangle):
        return self.x >= rectangle.upper_left.x and self.x <= rectangle.upper_right.x and self.y >= rectangle.mid_down.y and self.y <= rectangle.upper_right.y

    def distance_to_rectangle(self, rect):
        if self.y < rect.mid_down.y:
            return self.distance_to_point(rect.mid_down)
        if self.x < rect.upper_left.x:
            return self.distance_to_point(rect.upper_left)
        if self.x > rect.upper_right.x:
            return self.distance_to_point(rect.upper_right)
        return 0, None

class Rectangle:
    def __init__(self, upper_left, width, height):
        self.upper_left = upper_left
        self.upper_right = Point(upper_left.x + width, upper_left.y)
        self.mid_down = Point(upper_left.x + width/2, upper_left.y - height)
        self.width = width
        self.height = height

    def __repr__(self):
        x, y = self.upper_left.x, self.upper_left.y
        w, h = self.width, self.height
        return f'({x}, {y}): {w} X {h}'

LEFT = 0
RIGHT = 60
START = 25
FINISH = 100

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
        write(f"Position: {round(robot.x, 2), round(robot.y, 2)} ")
        shortest_distance, angle = robot.distance_to_rectangle(obstacles[0])
        for o in obstacles[1:]:
            d, a = robot.distance_to_rectangle(o)
            if d < shortest_distance:
                shortest_distance, angle = d, a

        # the borders are also objects
        d, a = RIGHT - robot.x, 0
        if d < shortest_distance:
            shortest_distance, angle = d, a
        d, a = robot.x - LEFT, 180
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
        new_position = Point(robot.x + cos(new_direction_angle), robot.y + sin(new_direction_angle))
        robot = new_position

        fail = False
        # Check if a colission has been ocurred
        for o in obstacles:
            fail |= robot.is_inside_of(o)
        fail |= robot.x >= RIGHT or  robot.x <= LEFT
        if fail:
            write(f"FAIL!!!!!!!!!!!!!. Object: {o}\n\n\n\n")
            return "fail"

        # remove passed objects
        new_obstacles = []
        for o in obstacles:
            if o.upper_left.y >= robot.y:
                new_obstacles.append(o)
        obstacles = new_obstacles

    return "success"


def set_obstacles():
    obstacles = []
    no_obstacles = 10
    write(f"Obstacles:\n")
    for _ in range (no_obstacles):
        w = random.randint(3, 10)
        h = random.randint(3, 10)
        x = random.randint(LEFT, RIGHT)
        y = random.randint(START, FINISH)
        r = Rectangle(Point(x, y), w, h)
        write(f"{r}\n")
        obstacles.append(r)
    write('\n\n')
    return obstacles


def perform_simulations(no_simulations):
    inference_methods = ["Mamdani", "Larsen"]
    defuzzification_methods = ["coa", "boa"]
    results = {(im, dm): 0 for im in inference_methods for dm in defuzzification_methods}

    for i in range(no_simulations):
        print(f"Simulation #{i}\n")
        write(f"\n\n--------------------------Simulation #{i}-------------------\n\n")
        obstacles = set_obstacles()
        for im in inference_methods:
            for dm in defuzzification_methods:
                write(f'{im}, {dm}\n')
                robot = Point((LEFT+RIGHT)/2, 0)
                obstacles_copy = list(obstacles)
                result = simulate(robot, obstacles_copy, inference_method=im, defuzzification_method=dm)
                if result == "fail":
                    results[im, dm] += 1
                else:
                    write('SUCCESS!!!!!!!!!\n\n\n\n')

    return results


results = perform_simulations(10)
print(results)
