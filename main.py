'''
EN.640.635 Software Carpentry
Final project
This Python file defines the start of game, and some set-up,
including game time limit and speed of fish.
'''
from myfish import *

if __name__ == '__main__':
    # Set up the time to complete game (unit: seconds)
    time = 100
    # Set up the speed of fish
    speed = 500

    # Start the game
    run(time_count=time, fish_speed=speed)
