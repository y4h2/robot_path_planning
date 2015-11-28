# Author: Yu Huang

from controller import Controller
import math
import numpy
import random
from math import sqrt
from random import randint

class PathPlanning(Controller):
    """Path planning with genetic algorithm"""
    
    def __init__(self, params):
        """Initialize internal variables"""

        Controller.__init__(self,params)
        
        # This angle shows the direction that the controller
        # tries to follow. It is used by the supervisor
        # to draw and debug this controller
        self.heading_angle = 0
    
    def restart(self):
        pass
    
    # generate some random points (the number as an input)
    def set_parameters(self, params):
        """set path planning values"""
        pass
        # mutate rate
        # cross_over rate
     
    def get_parameters(self, state):
        #get goal
        goal = (state.goal.x, state.goal.y)
         
        # start point
        #(x_r, y_r, theta) = state.pose
        start = (0.0, 0.0)

    def execute(self, state, dt):
        goal = (state.goal.x, state.goal.y)
        
        start = (0.0, 0.0)
        print 'goal is', goal
        print 'start point is ', start
        # TODO read vertext point from world file
        vertexs = [(2,3), (3,2), (2,2), (3,3)]
        pop = population(20, 2, start, goal)
        for i in range(100):
            parents = evolve(pop, start, goal, vertexs)


        """
        only use first individual as path
        best_individual is a list with mid_point
        start point and goal are not included
        """
        best_individual = parents[0]
        # for mid_point in best_individual:

        #return a list of mid_point
        print best_individual
        print fitness(best_individual, start, goal, vertexs)
        return 0,0

# genetic algorithm


def individual (length, start, goal, precise = 1):
    """Create a member of the population"""
    return [ (round(random.uniform(start[0],goal[0]), precise), round(random.uniform(start[0], goal[0]), precise)) for i in xrange(length) ]
    
def population(count, length, start, goal):
    """
    Create a number of individuals (i.e. a population).

    count: the number of individuals in the population
    length: the number of values per individual
    min: the min possible value in an individual's list of values
    max: the max possible value in an individual's list of values
 
    """
    return [ individual(length, start, goal) for i in xrange(count) ]
  

# fitness function to be changed later
def fitness(individual,start, goal, vertexs):
    """
    Determine the fitness of an individual. Lower is better.

    individual: the individual to evaluate
    target: the sum of numbers that individuals are aiming for
    """
    #TODO
    previous_point = (start[0], start[1])
    sum = 0.0
    for point in individual:
        sum += sqrt((point[0] - previous_point[0])**2 +(point[1] - previous_point[1])**2 )
        if collision_detect(vertexs, previous_point, point):
            sum += 100 # depends on the scale of problem
        previous_point = point
    
    sum += sqrt((goal[0] - previous_point[0])**2 + (goal[1] - previous_point[1])**2)
    if collision_detect(vertexs, previous_point, goal):
        sum += 100
    return sum

# evolution operations
def evolve(pop, start, goal, vertexs, retain=0.9, random_select=0.05, mutate=0.01, crossover_pos=None, precise=1):
    graded = [ (fitness(x, start, goal, vertexs), x) for x in pop]
    graded = [ x[1] for x in sorted(graded)]
    retain_length = int(len(graded)*retain)
    parents = graded[:retain_length]

    # randomly add other individuals to promote genetic diversity
    for individual in graded[retain_length:]:
        if random_select > random.random():
            parents.append(individual)

    # mutate some individuals
    for individual in parents:
        if mutate > random.random():
            pos_to_mutate = randint(0, len(individual)-1)
            # this mutation is not ideal, because it
            # restricts the range of possible values,
            # but the function is unaware of the min/max
            # values used to create the individuals,
            individual[pos_to_mutate] = (round(random.uniform(start[0], goal[0]), precise), \
                                            round(random.uniform(start[1], goal[1]), precise))

    # crossover parents to create children
    parents_length = len(parents)
    desired_length = len(pop) - parents_length
    children = []
    while len(children) < desired_length:
        male = randint(0, parents_length-1)
        female = randint(0, parents_length-1)
        if male != female:
            male = parents[male]
            female = parents[female]
            if crossover_pos == None:
                crossover_pos = len(male) / 2
            child = male[:crossover_pos] + female[crossover_pos:]
            children.append(child)

    parents.extend(children)
    return parents

    
"""
    collision detect
    input: obstacles' vertex coordinates, list vertex_list[]
"""


# point1,point2 are tuples
def collision_detect(vertexs, point1, point2):
    positive_flag = 0
    negative_flag = 0
    step_b = False
    # line function
    line = lambda x1, y1, x2, y2, x, y: (y2-y1)*x + (x1-x2)*y + (x2*y1 - x1*y2)
    for vertex in vertexs:
        if line(point1[0], point1[1],point2[0], point2[1], vertex[0], vertex[1]) == 0:
            step_b = True
            break
        elif line(point1[0], point1[1],point2[0], point2[1], vertex[0], vertex[1]) < 0:
            negative_flag += 1
        else:
            positive_flag += 1
    if step_b or (not step_b and (positive_flag * negative_flag) != 0):
        max_x = 0.0
        max_y = 0.0
        min_x = 100.0 
        min_y = 100.0
        for vertex in vertexs:
            max_x = max(max_x, vertex[0])
            min_x = min(min_x, vertex[0])
            max_y = max(max_y, vertex[1])
            min_y = min(min_y, vertex[1])
        if (point1[0] > max_x and point2[0] > max_x) or \
            (point1[0] < min_x and point2[0] < min_x) or \
            (point1[1] > max_y and point2[1] > max_y) or \
            (point1[1] < min_y and point2[1] < min_y):
            return False
        else:
            return True
    else:
        return False
        