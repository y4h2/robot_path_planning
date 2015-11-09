# input a matrix's shape, x, y

from random import randint
import random
from math import sqrt

vertexs = [(2,3), (3,2), (2,2), (3,3)]
class GeneticFunction(object):
	
	def __init__(self, mutate_rate=0.01,start=(0.0, 0.0), goal=(3.0, 3.0), precise=1, retain_rate=0.2):
		self.mutate_rate = mutate_rate
		self.start = start
		self.goal = goal
		self.precise = precise
		self.retain_rate = retain_rate
		
	
	
	def mutation(self, individual):
		if self.mutate_rate > random.random():
			pos_to_mutate = randint(0, len(individual)-1)
			individual[pos_to_mutate] = (round(random.uniform(self.start[0], self.goal[0]),self.precise), 
										round(random.uniform(self.start[0], self.goal[0]),self.precise))
		return individual
		
	def select(self, population):
		graded_pop = [ (self.fitness(x), x) for x in population]
		graded_pop = [ x[1] for x in sorted(graded_pop)]
		retain_length = int(len(population)*self.retain_rate)
		retain_pop = graded_pop[:retain_length]
		return retain_pop
		
		
	def crossover(self, population, crossover_pos=None):
		population_length = len(population)
		male_pos = randint(0, population_length-1)
		female_pos = randint(0, population_length-1)
		children = []
		if male_pos != female_pos:
			male = population[male_pos]
			female = population[female_pos]
			if crossover_pos == None:
				crossover_pos = len(male) / 2
			child = male[:crossover_pos] + female[crossover_pos:]
			children.append(child)

		population.extend(children)
		return population

	def fitness(self, individual):
		"""
		#Determine the fitness of an individual. Lower is better.

		#individual: the individual to evaluate
		#target: the sum of numbers that individuals are aiming for
		"""
		#TODO
		previous_point = self.start
		sum = 0.0
		for point in individual:
			sum += sqrt((point[0] - previous_point[0])**2 +(point[1] - previous_point[1])**2 )
			if collision_detect(vertexs, previous_point, point):
				sum += 100 # depends on the scale of problem
			previous_point = point
		
		sum += sqrt((self.goal[0] - previous_point[0])**2 + (self.goal[1] - previous_point[1])**2)
		if collision_detect(vertexs, previous_point, self.goal):
			sum += 100
		return sum
		
	
def collision_detect(vertexs, point1, point2):
	positive_flag = 0
	negative_flag = 0
	step_b = False
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









'''

def individual (length, xmax, ymax):
	'Create a member of the population'
	return [ (round(random.uniform(0.0,xmax), 1), round(random.uniform(0.0, ymax), 1)) for i in xrange(length) ]
	
def population(count, length, xmax, ymax):
	"""
    #Create a number of individuals (i.e. a population).

    #count: the number of individuals in the population
    #length: the number of values per individual
    #min: the min possible value in an individual's list of values
    #max: the max possible value in an individual's list of values
 
    """
	return [ individual(length, xmax, ymax) for i in xrange(count) ]
  

# fitness function to be changed later


# evolution operations
def evolve(pop, retain=0.9, random_select=0.05, mutate=0.01):
    

    # randomly add other individuals to promote genetic diversity
    for individual in graded[retain_length:]:
        if random_select > random.random():
            parents.append(individual)

    
        
    # crossover parents to create children
    
    return parents

	
"""
	#collision detect
	#input: obstacles' vertex coordinates, list vertex_list[]
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
	
'''
		

	
'''
if __name__ == "__main__":
	vertexs = [(2,3), (3,2), (2,2), (3,3)]
	pop = population(20,2, 3.0, 3.0)
	for i in range(100):
		parents = evolve(pop)

		
	for ind in parents:
		print fitness(ind)
		print ind
		print '\n'
	
	
'''