'''
EN.640.635 Software Carpentry
Final project
This Python file defines a winning condition for the mission.
and fails if the time is out.
The file includes functions for initializing the simulation,
updating object positions, handling collisions,
and determining mission completion.
'''
import pygame
from strategy import strategy
from move import move, set_move_last
from collision import final_is_colliding, AfterCollision
from mission import *


def step():
    """
    Perform one step of the simulation.

    Returns:
        bool: True if the mission is complete, False otherwise
    """
    # Implement Strategy for each robotfish
    for a in father_obj:
        if a.name == "robotfish":
            a.v_mode, a.w_mode, a.w_dot_direction = strategy(a)
            print(a.v_mode)

    # Save current position and orientation for all objects
    for a in all_obj:
        a.x_last, a.y_last, a.theta_last = a.x, a.y, a.theta

    # Move each object based on its velocity and angular velocity
    for a in father_obj:
        a.colliding_list.clear()
        move(a, timestep)

    # Collision detection and handling loop
    c_flag = 1
    n = 0
    while c_flag == 1 and n <= 1:
        n += 1
        _father_obj = father_obj.copy()
        c_flag = 0
        for a in father_obj:
            _father_obj.remove(a)
            for b in _father_obj:
                # Check for collisions between objects
                result = final_is_colliding(a, b)
                if result is not False:
                    c_flag = 1
                    a, b = result[1], result[2]
                    Flag = "a" if b.shape != "circle" and not a.fixed else "b"

                    # Perform actions after collision based on calculation flag
                    if a.collision_calculation and b.collision_calculation:
                        AfterCollision(a, b) if Flag == "a" \
                            else AfterCollision(b, a)

    # Update the last position and orientation for all objects
    for a in all_obj:
        set_move_last(a)

    # Move each object again based on updated position and orientation
    for a in father_obj:
        move(a, timestep)

    # Check if the mission is complete
    return win()


def run(time_count, fish_speed):
    """
    Run the simulation with a given time limit.
    This function initializes the simulation, sets up the Pygame display, and
    runs the main simulation loop.

    Parameters:
        time_count (int): The time limit for the simulation in seconds.
        fish_speed (int): The speed for fish moving.
    """
    # Initialize mission parameters and Pygame
    mission()
    pygame.init()
    screen = pygame.display.set_mode((border_x, border_y), 0, 32)
    clock = pygame.time.Clock()
    pygame.display.set_caption(task_name)
    pause_flag = 1
    result = False
    start_time = pygame.time.get_ticks()
    # Set the font style and size for displaying text
    font = pygame.font.SysFont('microsoft Yahei', 50)
    # Create a text surface for the "Complete" message with blue color
    text_win = font.render("Complete", False, (0, 0, 255))
    # Create a text surface for the "Complete" message with blue color
    text_False = font.render("Time out, try again!!!", False, (0, 0, 255))

    # Flag to indicate if the game is over (win or timeout)
    game_over = False

    while True:
        current_time = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                # Exit the function
                return

        if not game_over:
            # Calculate elapsed time and remaining time
            elapsed_time = (current_time - start_time) / 1000
            remaining_time = max(time_count - elapsed_time, 0)

        if result:
            # Display "Complete" message if the mission is complete
            screen.blit(text_win, (500, 250))
            pygame.display.flip()
            # Set the game over flag
            game_over = True

        elif remaining_time <= 0 and not game_over:
            # Display "Time out, try again!!!" message if time limit is reached
            screen.blit(text_False, (500, 250))
            pygame.display.flip()
            # Set the game over flag
            game_over = True

        if not game_over:
            if pause_flag == 1:
                # Clear the screen and update simulation at each time step
                screen.fill((173, 216, 250))
                global th
                th += 1
                print("*" * 10, th, "*" * 10)
                result = step()

                # Display the countdown timer
                timer_text = font.render(f"Time Left: {remaining_time:.2f}",
                                         False, (255, 0, 0))
                # Adjust position as needed
                screen.blit(timer_text, (10, 10))

                # Draw objects based on their types (circle or polygon)
                for a in obj_draw:
                    if a in obj_circle:
                        if a.mass == 0:
                            # Draw circle for objects with mass 0
                            pygame.draw.circle(screen, a.color,
                                               (int(
                                                   a.realtime_points['p0'][0]
                                               ),
                                                   int(
                                                   a.realtime_points['p0'][1])
                                               ),
                                               int(
                                                   a.radius + a.draw_radius), 1
                                               )
                        elif a.mass != 0:
                            # Draw circle for objects with non-zero mass
                            pygame.draw.circle(screen, a.color,
                                               (int(
                                                   a.realtime_points['p0'][0]
                                               ),
                                                   int(
                                                   a.realtime_points['p0'][1])
                                               ),
                                               int(a.radius))
                    elif a in obj_polygon:
                        # Draw polygons
                        pygame.draw.polygon(
                            screen, a.color,
                            tuple(a.realtime_points.values()), 0)

        if game_over:
            # Check for a key press or some other event to exit after game over
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN or event.type == pygame.QUIT:
                    pygame.quit()
                    # Exit the function
                    return

        clock.tick(fish_speed)
        pygame.display.update()


if __name__ == '__main__':
    run(time_count=30, fish_speed=200)
