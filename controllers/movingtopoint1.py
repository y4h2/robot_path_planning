# modified by Yu Huang
from controllers.pid_controller import PIDController
import math
import numpy


class MovingToPoint1(PIDController):
    """FollowPath (i.e. move to next point) steers the robot to a predefined position in the world."""
    def __init__(self, params):
        """Initialize internal variables"""
        PIDController.__init__(self,params)
        self.params = params
        #print params.path

    def get_heading_angle(self, state):
        """Get the direction from the robot to the goal as a vector."""
        
        # generate heading angle to the next point
        x_g, y_g = self.params.path[0][0], self.params.path[0][1]
        #print point_cnt, 'FollowPath'
        # The robot:
        x_r, y_r, theta = state.pose

        # Where is the goal in the robot's frame of reference?
        return (math.atan2(y_g - y_r, x_g - x_r) - theta + math.pi)%(2*math.pi) - math.pi

    def get_heading(self,state):
        goal_angle = self.get_heading_angle(state)
        return numpy.array([math.cos(goal_angle),math.sin(goal_angle),1])
    
    def execute(self, state, dt):
        v, w = PIDController.execute(self, state, dt)
        #print 'Move to point ', (self.params.ga_path[point_cnt][0], self.params.ga_path[point_cnt][1])
        
        return v, w