# input a matrix's shape, x, y

from random import randint
import random
def individual (length, xmax, ymax):
	'Create a member of the population'
	return [ (randint(0,xmax)/10.0, randint(0, ymax)/10.0) for i in xrange(length) ]
	
def population(count, length, xmax, ymax):
	"""
    Create a number of individuals (i.e. a population).

    count: the number of individuals in the population
    length: the number of values per individual
    min: the min possible value in an individual's list of values
    max: the max possible value in an individual's list of values
 
    """
	return [ individual(length, xmax, ymax) for i in xrange(count) ]
  
from math import sqrt
# fitness function to be changed later
def fitness(individual):
	"""
    Determine the fitness of an individual. Lower is better.

    individual: the individual to evaluate
    target: the sum of numbers that individuals are aiming for
    """
	#TODO
	start_x = 0.0
	start_y = 0.0
	goal_x = 3.0
	goal_y = 3.0
	sum = 0.0

	for x,y in individual:
		sum += sqrt((x - start_x)**2 + (y - start_y)**2)
		start_x = x
		start_y = y
		
	sum += sqrt((goal_x - start_x)**2 + (goal_y - start_y)**2)
	return sum

# evolution operations
def evolve(pop, retain=0.9, random_select=0.05, mutate=0.01):
    graded = [ (fitness(x), x) for x in pop]
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
            individual[pos_to_mutate] = (round(random.uniform(min(individual[0]), max(individual[0])),1), 
										round(random.uniform(min(individual[1]), max(individual[1])),1))

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
            half = len(male) / 2
            child = male[:half] + female[half:]
            children.append(child)

    parents.extend(children)
    return parents
	
	
if __name__ == "__main__":
	pop = population(20,2, 30, 30)
	for i in range(100):
		parents = evolve(pop)

		
	for ind in parents:
		print fitness(ind)
		print ind
		print '\n'
	