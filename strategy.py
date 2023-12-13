'''
EN.640.635 Software Carpentry
Final project
This Python file defines strategies for controlling a robot fish in a 2D simulation environment using the Pygame library. 
The primary focus is to guide the robot fish towards a target, typically the mouse cursor, 
and manage its velocity and orientation based on its current state and the target's position.
'''
import util
from env import *
import math
import pygame

def strategy(a):
    """
    Define the strategy for the robot fish.

    Parameters:
        a (object): The robot fish object

    Returns:
        tuple: A tuple containing the velocity mode, angular velocity mode, and angular velocity direction
    """
    if a.name == "robotfish":
        aiming_theta, distance = move_to_mouse_position(a)
        a_w_dot_direction = get_direction_of_theta_to_theta(a.theta, aiming_theta)

        # If the robot fish is pointing in the aiming direction and has low velocity
        if math.fabs(a.theta - aiming_theta) < 0.1 and a.v < 20:
            a_v_mode = 2  # Accelerate
            a_w_mode = 0  # Do not rotate

        # If the robot fish is pointing in the aiming direction and has sufficient velocity
        elif math.fabs(a.theta - aiming_theta) < 0.1 and a.v >= 20:
            a_v_mode = 1  # Maintain velocity
            a_w_mode = 0  # Do not rotate

        # If the robot fish needs to adjust its direction
        else:
            a_v_mode = 0  # Do not change velocity
            a_w_mode = 1  # Rotate to adjust direction

        return a_v_mode, a_w_mode, a_w_dot_direction

def move_to_mouse_position(a):
    """
    Calculate the aiming direction and distance based on the mouse position.

    Parameters:
        a (object): The robot fish object

    Returns:
        tuple: A tuple containing the aiming direction (theta) and distance to the mouse position
    """
    mouse_position = pygame.mouse.get_pos()
    position_vector = (mouse_position[0] - a.x, mouse_position[1] - a.y)
    distance = util.get_norm_of_vector(position_vector)
    direction = util.get_direction_vector(position_vector)
    theta = util.get_theta_of_vector(direction)

    return theta, distance
