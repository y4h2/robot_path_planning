# genetic algorithm
from collision_detect import collision_detect
import random
from math import sqrt
from random import randint



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

def ga_execute(start, goal):
    vertexs = [(2,3), (3,2), (2,2), (3,3)]
    pop = population(20, 2, start, goal)
    for i in range(100):
        parents = evolve(pop, start, goal, vertexs)

    
    best_individual = parents[0]

    print fitness(best_individual, start, goal, vertexs)
    
    return best_individual
