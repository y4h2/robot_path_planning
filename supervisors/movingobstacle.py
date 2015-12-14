#modified by Yu Huang
from khepera3 import K3Supervisor
from supervisor import Supervisor
from math import sqrt, sin, cos, atan2
import numpy

class K3FullSupervisor(K3Supervisor):
    """K3Full supervisor implements the full switching behaviour for navigating labyrinths."""
    def __init__(self, robot_pose, robot_info):
        """Create controllers and the state transitions"""
        K3Supervisor.__init__(self, robot_pose, robot_info)

        # The maximal distance to an obstacle (inexact)
        self.distmax = robot_info.ir_sensors.rmax + robot_info.wheels.base_length/2

        # Fill in some parameters
        self.parameters.sensor_poses = robot_info.ir_sensors.poses[:]
        self.parameters.ir_max = robot_info.ir_sensors.rmax
        self.parameters.direction = 'left'
        self.parameters.distance = self.distmax*0.85
        self.parameters.path = [(1.0, 0.5), (0.5, 1.0)]
        self.process_state_info(robot_info)
        
        #Add controllers
        self.movingtopoint1 = self.create_controller('MovingToPoint1', self.parameters)
        self.movingtopoint2 = self.create_controller('MovingToPoint2', self.parameters)
        # Define transitions
       
        self.add_controller(self.movingtopoint1,
                             (self.at_point1, self.movingtopoint2))
        self.add_controller(self.movingtopoint2,
                             (self.at_point2, self.movingtopoint1))
        # Start in the 'go-to-goal' state
        self.current = self.movingtopoint1

    def set_parameters(self,params):
        """Set parameters for itself and the controllers"""
        K3Supervisor.set_parameters(self,params)
        self.movingtopoint1.set_parameters(self.parameters)
        self.movingtopoint2.set_parameters(self.parameters)
    
    def at_point1(self):
        """Check if the distance to point1 is small"""
        return  sqrt((self.pose_est.x - self.parameters.path[0][0])**2 + (self.pose_est.y - self.parameters.path[0][1])**2) < self.robot.wheels.base_length/2

    def at_point2(self):
        """Check if the distance to point2 is small"""
        return  sqrt((self.pose_est.x - self.parameters.path[1][0])**2 + (self.pose_est.y - self.parameters.path[1][1])**2) < self.robot.wheels.base_length/2


  
    def process_state_info(self, state):
        """Update state parameters for the controllers and self"""

        K3Supervisor.process_state_info(self,state)

        # The pose for controllers
        self.parameters.pose = self.pose_est
        
        # Distance to the goal
        self.distance_from_goal = sqrt((self.pose_est.x - self.parameters.goal.x)**2 + (self.pose_est.y - self.parameters.goal.y)**2)
        
        # Sensor readings in real units
        self.parameters.sensor_distances = self.get_ir_distances()
        
        # Smallest reading translated into distance from center of robot
        vectors = \
            numpy.array(
                [numpy.dot(
                    p.get_transformation(),
                    numpy.array([d,0,1])
                    )
                     for d, p in zip(self.parameters.sensor_distances, self.parameters.sensor_poses) \
                     if abs(p.theta) < 2.4] )
        
        self.distmin = min((sqrt(a[0]**2 + a[1]**2) for a in vectors))
    
    def draw(self, renderer):
        """Draw controller info"""
        K3Supervisor.draw(self,renderer)

        renderer.set_pose(self.pose_est)
        arrow_length = self.robot_size*5

        if self.current == self.gtg:
            # Draw arrow to goal
            renderer.set_pen(0x00FF00)
            renderer.draw_arrow(0,0,
                arrow_length*cos(self.gtg.heading_angle),
                arrow_length*sin(self.gtg.heading_angle))

        elif self.current == self.avoidobstacles:
            # Draw arrow away from obstacles
            renderer.set_pen(0xFF0000)
            renderer.draw_arrow(0,0,
                arrow_length*cos(self.avoidobstacles.heading_angle),
                arrow_length*sin(self.avoidobstacles.heading_angle))

        elif self.current == self.wall:

            # Draw vector to wall:
            renderer.set_pen(0x0000FF)
            renderer.draw_arrow(0,0,
                self.wall.to_wall_vector[0],
                self.wall.to_wall_vector[1])
            # Draw 
            renderer.set_pen(0xFF00FF)
            renderer.push_state()
            renderer.translate(self.wall.to_wall_vector[0], self.wall.to_wall_vector[1])
            renderer.draw_arrow(0,0,
                self.wall.along_wall_vector[0],
                self.wall.along_wall_vector[1])
            renderer.pop_state()

            # Draw heading (who knows, it might not be along_wall)
            renderer.set_pen(0xFF00FF)
            renderer.draw_arrow(0,0,
                arrow_length*cos(self.wall.heading_angle),
                arrow_length*sin(self.wall.heading_angle))

            # Important sensors
            renderer.set_pen(0)
            for v in self.wall.vectors:
                x,y,z = v
                
                renderer.push_state()
                renderer.translate(x,y)
                renderer.rotate(atan2(y,x))
            
                renderer.draw_line(0.01,0.01,-0.01,-0.01)
                renderer.draw_line(0.01,-0.01,-0.01,0.01)
                
                renderer.pop_state()