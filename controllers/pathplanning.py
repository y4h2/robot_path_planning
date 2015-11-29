# Author: Yu Huang

from controller import Controller
import math
import numpy
from math import sqrt
import genetic_algorithm as ga

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
       
        """
        only use first individual as path
        best_individual is a list with mid_point
        start point and goal are not included
        """
        # for mid_point in best_individual:
        best_individual = ga.ga_execute(start, goal)
        #return a list of mid_point
        print best_individual
        
        return 0, 0


    

