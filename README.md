# Final project for EN.540.635 at JHU
# Bionic Fish
## Abstract
This project proposal outlines the development of a 2D game utilizing the pygame module
in Python. The game will be task-oriented, featuring an Bionic Fish agent controlled by a
single player to complete various missions. The objective is to create an engaging and
challenging gaming experience, leveraging the capabilities of pygame for seamless
development and execution.

## Team Member
- Chong-Tong Chow: cchow14@jhu.edu  
- Nianxiang Xu: nxu21@jhu.edu

## Game Overview
Upon launching main.py, players are introduced to a countdown timer.  

The target is using mouse to maneuver the fish to bump balls into designated target points within the allotted time. Succeeding in this task results in victory, while failure to do so before time expires means defeat.
  
  
  
![image](https://github.com/chowchongtong/BionicFish/assets/74456922/dfeb255d-8386-44e1-8f9d-22358f8e5279)

## Feature - Controls and Mechanics
- The bionic fish follows the movement of the mouse.  
- Interaction with objects triggers the collision algorithm from collision.py, simulating realistic physical impacts.  
- Effects of collisions vary based on the angle of impact and the relative masses of the objects involved.  
- Players can adjust the fish's speed and the countdown timer to modify the game's difficulty.  
- The quantity of balls and target points can be increased to add complexity.  

## Requirements
To run this game, ensure you have Python 3 and Pygame installed on your system.

- Setup
1. Install Python3 if you haven't already.
2. Install math if you haven't already.
3. Install Pygame using pip: pip install pygame
- Run
1. Clone the repository or download the game files to your local machine.
2. Navigate to the game directory in your terminal.
3. Run the game with: python main.py

## File Descriptions
- env.py: Contains environment variables and game settings.
- function.py: Helper functions for various game tasks.
- myfish.py: Defines the fish's behavior and properties and task.
- util.py: Utility functions for general purposes.
- strategy.py: Holds the game's strategic elements and mechanics, including fish's control under mouse.
- move.py: Manages the movement and control of game entities.
- mission.py: Defines the mission objectives and conditions.
- collision.py: Collision detection and physics simulation.
- main.py: Start file.

## Design Philosophy
The design concept of this bionic robotic fish draws inspiration from the traditional Chinese koi fish color palette.  

Incorporating the rich symbolism associated with koi, the color scheme not only pays homage to cultural traditions but also symbolizes attributes such as perseverance, prosperity, and good fortune. The vibrant hues of the koi-inspired design aim to create an aesthetically pleasing and culturally resonant robotic fish.  

<img width="97" alt="image" src="https://github.com/chowchongtong/BionicFish/assets/74456922/6e190330-6a92-43c7-a9fc-a7ec9073c952">


## Reference
Thanks to Zhichao Quan's effort in collision simulation.  

Zhichao is research partner of Chong-Tong in his undergradute period. His major in Theoretical Mechanics, and he is good at mechanical problem. 

In the previous period, Zhichao provided guidance to Chong-Tong in simulating object collisions through code, making significant contributions to the object collision simulation in this current project.

## Support
For questions, issues, or support regarding the game, please open an issue in the repository or contact the maintainers.

Enjoy the underwater adventure with RobotFish!

