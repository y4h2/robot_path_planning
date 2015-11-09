# Author: Yu Huang

from controller import Controller
import math
import numpy

class PathPlanning(Controller):
	"""Path planning with genetic algorithm"""
	
	def __init__(self, params):
        '''Initialize internal variables'''
        Controller.__init__(self,params)
        
        # This angle shows the direction that the controller
        # tries to follow. It is used by the supervisor
        # to draw and debug this controller
        self.heading_angle = 0
	
	def restart(self):
		
	
	# generate some random points (the number as an input)
	def set_parameters(self, params):
		"""set path planning values"""
		self.point_num = params.point_num
		# ±äÒìÂÊ
		# cross_over rate
	 
	 
	 # genetic algorithm
	 from random import randint
	def individual (length, min, max):
		'Create a member of the population'
		return [ randint(min,max) for x in xrange(length) ]
		
	def population(count, length, min, max):
		"""
		Create a number of individuals (i.e. a population).

		count: the number of individuals in the population
		length: the number of values per individual
		min: the min possible value in an individual's list of values
		max: the max possible value in an individual's list of values
	 
		"""
		return [ individual(length, min, max) for x in xrange(count) ]
		
	from operator import add
	def fitness(individual, target):
		"""
		Determine the fitness of an individual. Lower is better.

		individual: the individual to evaluate
		target: the sum of numbers that individuals are aiming for
		"""
		sum = reduce(add, individual, 0)
		return abs(target-sum)
		
	def grade(pop, target):
		'Find average fitness for a population.'
		summed = reduce(add, (fitness(x, target) for x in pop), 0)
		return summed / (len(pop) * 1.0)

	# evolution operations
	def evolve(pop, target, retain=0.2, random_select=0.05, mutate=0.01):
		graded = [ (fitness(x, target), x) for x in pop]
		graded = [ x[1] for x in sorted(graded)]
		retain_length = int(len(graded)*retain)
		parents = graded[:retain_length]

		# randomly add other individuals to promote genetic diversity
		for individual in graded[retain_length:]:
			if random_select > random():
				parents.append(individual)

		# mutate some individuals
		for individual in parents:
			if mutate > random():
				pos_to_mutate = randint(0, len(individual)-1)
				# this mutation is not ideal, because it
				# restricts the range of possible values,
				# but the function is unaware of the min/max
				# values used to create the individuals,
				individual[pos_to_mutate] = randint(
					min(individual), max(individual))

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