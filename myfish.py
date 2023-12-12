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
    text_pause = font.render("pause", False, (0, 0, 255))

    while True:
        if result:
            screen.blit(text_win, (500, 250))
            pygame.display.flip()
            pause_flag *= -1
            result = False
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Toggle pause when the mouse is clicked
                    pause_flag *= -1
                    screen.blit(text_pause, (int(border_x * 7 / 8), int(border_y * 7 / 8)))
                    print("pause")

            if pause_flag == 1:
                screen.fill((255, 255, 255))
                global th
                th += 1
                print("*" * 10, th, "*" * 10)
                result = step()

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

            clock.tick(500)
            pygame.display.update()

if __name__ == '__main__':
    run()
