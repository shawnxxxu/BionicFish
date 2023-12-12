import pygame
from strategy import strategy
from move import move, set_move_last
from collision import final_is_colliding, AfterCollision
from mission import *

def step():
    # Implement Strategy
    for a in father_obj:
        if a.name == "robotfish":
            a.v_mode, a.w_mode, a.w_dot_direction = strategy(a)
            print(a.v_mode)

    for a in all_obj:
        # Save current position and orientation for all objects
        a.x_last, a.y_last, a.theta_last = a.x, a.y, a.theta

    for a in father_obj:
        a.colliding_list.clear()
        move(a, timestep)

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
                if result != False:
                    c_flag = 1
                    a, b = result[1], result[2]
                    Flag = "a" if b.shape != "circle" and not a.fixed else "b"

                    if a.collision_calculation and b.collision_calculation:
                        AfterCollision(a, b) if Flag == "a" else AfterCollision(b, a)

    for a in all_obj:
        set_move_last(a)

    for a in father_obj:
        move(a, timestep)

    return win()


def run():
    mission()
    pygame.init()
    screen = pygame.display.set_mode((border_x, border_y), 0, 32)
    clock = pygame.time.Clock()
    pygame.display.set_caption(task_name)
    pause_flag = 1
    result = False
    font = pygame.font.SysFont('microsoft Yahei', 50)
    text_win = font.render("complete", False, (0, 0, 255))
    text_False = font.render("Time out, try again!!!", False, (0, 0, 255))
    countdown_duration = 20
    start_time = pygame.time.get_ticks()
    game_over = False  # Flag to indicate if the game is over (win or timeout)

    while True:
        current_time = pygame.time.get_ticks()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return  # Exit the function

        if not game_over:
            elapsed_time = (current_time - start_time) / 1000
            remaining_time = max(countdown_duration - elapsed_time, 0)

        if result:
            screen.blit(text_win, (500, 250))
            pygame.display.flip()
            game_over = True  # Set the game over flag

        elif remaining_time <= 0 and not game_over:
            screen.blit(text_False, (500, 250))
            pygame.display.flip()
            game_over = True  # Set the game over flag

        if not game_over:
            if pause_flag == 1:
                screen.fill((255, 255, 255))
                global th
                th += 1
                print("*" * 10, th, "*" * 10)
                result = step()
                                
                # Display the countdown timer
                timer_text = font.render(f"Time Left: {remaining_time:.2f}", False, (255, 0, 0))
                screen.blit(timer_text, (10, 10))  # Adjust position as needed

                for a in obj_draw:
                    if a in obj_circle:
                        if a.mass == 0:
                            # Draw circle for objects with mass 0
                            pygame.draw.circle(screen, a.color,
                                               (int(a.realtime_points['p0'][0]), int(a.realtime_points['p0'][1])),
                                               int(a.radius + a.draw_radius), 1)
                        elif a.mass != 0:
                            # Draw circle for objects with non-zero mass
                            pygame.draw.circle(screen, a.color,
                                               (int(a.realtime_points['p0'][0]), int(a.realtime_points['p0'][1])),
                                               int(a.radius))
                    elif a in obj_polygon:
                        # Draw polygons
                        pygame.draw.polygon(screen, a.color, tuple(a.realtime_points.values()), 0)

        if game_over:
            # Check for a key press or some other event to exit after game over
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN or event.type == pygame.QUIT:
                    pygame.quit()
                    return  # Exit the function

        clock.tick(500)
        pygame.display.update()

if __name__ == '__main__':
    run()