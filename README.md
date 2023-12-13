# Final project for EN.540.635 at JHU
### Bionic Fish
## Abstract
This project proposal outlines the development of a 2D game utilizing the pygame module
in Python. The game will be task-oriented, featuring an Bionic Fish agent controlled by a
single player to complete various missions. The objective is to create an engaging and
challenging gaming experience, leveraging the capabilities of pygame for seamless
development and execution.

![image](https://github.com/chowchongtong/BionicFish/assets/74456922/dfeb255d-8386-44e1-8f9d-22358f8e5279)

## Team Member
- Chong-Tong Chow: cchow14@jhu.edu  
- Nianxiang Xu: nxu21@jhu.edu

## Game Overview
Upon launching main.py, players are introduced to a countdown timer. The objective is to maneuver the fish to bump balls into designated target points within the allotted time. Succeeding in this task results in victory, while failure to do so before time expires means defeat.
## Feature 
Controls and Mechanics
The bionic fish follows the movement of the mouse.
Interaction with objects triggers the collision algorithm from collision.py, simulating realistic physical impacts.
Effects of collisions vary based on the angle of impact and the relative masses of the objects involved.
Players can adjust the fish's speed and the countdown timer to modify the game's difficulty.
The quantity of balls and target points can be increased to add complexity.

## Requirements
To run this game, ensure you have Python 3 and Pygame installed on your system.

Setup
1. Install Python 3 if you haven't already.
2. Install Pygame using pip:
   
pip install pygame

1. Clone the repository or download the game files to your local machine.
2. Navigate to the game directory in your terminal.
3. Run the game with:

python main.py

## File Descriptions
env.py: Contains environment variables and game settings.
function.py: Helper functions for various game tasks.
myfish.py: Defines the fish's behavior and properties and task.
util.py: Utility functions for general purposes.
strategy.py: Holds the game's strategic elements and mechanics.
move.py: Manages the movement and control of game entities.
mission.py: Defines the mission objectives and conditions.
collision.py: Collision detection and physics simulation.
main.py: Start file.

## Reference

## Support
For questions, issues, or support regarding the game, please open an issue in the repository or contact the maintainers.

Enjoy the underwater adventure with RoboFish!

