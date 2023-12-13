'''
EN.640.635 Software Carpentry
Final project
This Python file defines functions for moving and updating objects within a simulation environment, particularly focusing on a robot fish. 
It includes methods for updating positions, velocities, and orientations of objects over time, as well as handling specific behaviors of the robot fish.
'''
from util import *


def move(a, timestep):
    """
    Update the position, orientation, and velocities of the object.

    Parameters:
        a (object): The object to be moved
        timestep (float): The time step for the movement update
    """
    # Update position and orientation
    a.x = a.x + a.x_dot * timestep
    a.y = a.y + a.y_dot * timestep
    a.theta = normalize_theta(a.theta + a.w * timestep)

    # Update velocities
    a.v = a.v + a.v * a.f * timestep
    a.w = a.w + a.w * a.f * timestep

    # Set x_dot and y_dot based on current velocity and orientation
    a.set_x_dot_and_y_dot()

    # Special handling for robotfish
    if a.name == "robotfish":
        # Update angular and linear velocities based on mode
        a.w_dot = a.w_dot_list[a.w_mode]
        a.v_dot = a.v_dot_list[a.v_mode]

        # Update orientation with angular velocity
        a.w = a.w + a.w_dot * a.w_dot_direction * timestep

        # Update x_dot and y_dot with linear velocity and orientation
        a.x_dot = a.x_dot + a.v_dot * math.cos(a.realtime_theta) * timestep
        a.y_dot = a.y_dot + a.v_dot * math.sin(a.realtime_theta) * timestep

        # Set v and theta_v based on updated velocities
        a.set_v_and_theta_v()

        # Perform tail waving for robotfish
        a.wave_tail()

    # Update the object
    update(a)


def move_next(a, move, timestep):
    """
    Move the current object and its children recursively.

    Parameters:
        a (object): The current object
        move (function): The move function to be applied
        timestep (float): The time step for the movement update
    """
    move(a, timestep)
    # Move each child recursively
    if a.next != []:
        for i in a.next:
            move_next(i, move, timestep)


def set_move_last(a):
    """
    Set the object's position and orientation to its last state.

    Parameters:
        a (object): The object to be updated to its last state
    """
    a.theta = a.theta_last
    a.x = a.x_last
    a.y = a.y_last


def update(a):
    """
    Update the object's real-time properties.

    Parameters:
        a (object): The object to be updated
    """
    # Update real-time orientation for all objects
    a.realtime_theta = a.get_realtime_theta()

    # Special handling for robotfish
    if a.name == 'robotfish':
        a.update()

    # Update real-time points and core for all objects
    a.realtime_points = a.get_realtime_points()
    a.core = a.get_core()
