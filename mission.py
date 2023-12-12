from env import *

# Set up environment parameters
border_x = 1400
border_y = 800

ball_dx = 60
ball_dy = 40
ball1_x = int(border_x * 3 / 4 - ball_dx)
ball1_y = int(border_y / 2)
ball_r = 20
ball_color = (0, 100, 100)

fish_x = int(border_x / 6)
fish_y = int(border_y / 2)
fish_dx = 0
fish_dy = ball_dy

goal1_x = int(border_x / 2)
goal1_y = int(border_y / 2)
goal_dx = 90
goal_dy = 60
goal_r = 30
goal_color = (100, 0, 100)
task_name = "robotfish"


def mission():
    """
    Define mission environment with circles and goals.
    """
    width = 50

    # Define circles
    ball1 = Circle(name="ball", num=1, shape="circle", mass=1, n=1, relative_points={'p0': (0, 0)},
                   color=ball_color, x=ball1_x, y=ball1_y, x_dot=0, y_dot=0, radius=ball_r)

    ball2 = Circle(name="ball", num=2, shape="circle", mass=1, n=1, relative_points={'p0': (0, 0)},
                   color=ball_color, x=ball1_x + ball_dx, y=ball1_y + ball_dy, x_dot=0, y_dot=0, radius=ball_r)

    ball3 = Circle(name="ball", num=3, shape="circle", mass=1, n=1, relative_points={'p0': (0, 0)},
                   color=ball_color, x=ball1_x + ball_dx, y=ball1_y - ball_dy, x_dot=0, y_dot=0, radius=ball_r)

    ball4 = Circle(name="ball", num=4, shape="circle", mass=1, n=1, relative_points={'p0': (0, 0)},
                   color=ball_color, x=ball1_x + 2 * ball_dx, y=ball1_y + 2 * ball_dy, x_dot=0, y_dot=0, radius=ball_r)

    ball5 = Circle(name="ball", num=5, shape="circle", mass=1, n=1, relative_points={'p0': (0, 0)},
                   color=ball_color, x=ball1_x + 2 * ball_dx, y=ball1_y, x_dot=0, y_dot=0, radius=ball_r)

    ball6 = Circle(name="ball", num=6, shape="circle", mass=1, n=1, relative_points={'p0': (0, 0)},
                   color=ball_color, x=ball1_x + 2 * ball_dx, y=ball1_y - 2 * ball_dy, x_dot=0, y_dot=0, radius=ball_r)

    # Define goals
    goal1 = goal(name="goal", num=1, shape='circle', n=1, relative_points={'p0': (0, 0)}, color=goal_color,
                 x=goal1_x, y=goal1_y, x_dot=0, y_dot=0, draw_radius=goal_r)

    goal2 = goal(name="goal", num=2, shape='circle', n=1, relative_points={'p0': (0, 0)}, color=goal_color,
                 x=goal1_x - goal_dx, y=goal1_y + goal_dy, x_dot=0, y_dot=0, draw_radius=goal_r)

    goal3 = goal(name="goal", num=3, shape='circle', n=1, relative_points={'p0': (0, 0)}, color=goal_color,
                 x=goal1_x - goal_dx, y=goal1_y - goal_dy, x_dot=0, y_dot=0, draw_radius=goal_r)

    goal4 = goal(name="goal", num=4, shape='circle', n=1, relative_points={'p0': (0, 0)}, color=goal_color,
                 x=goal1_x - 2 * goal_dx, y=goal1_y + 2 * goal_dy, x_dot=0, y_dot=0, draw_radius=goal_r)

    goal5 = goal(name="goal", num=5, shape='circle', n=1, relative_points={'p0': (0, 0)}, color=goal_color,
                 x=goal1_x - 2 * goal_dx, y=goal1_y, x_dot=0, y_dot=0, draw_radius=goal_r)

    goal6 = goal(name="goal", num=6, shape='circle', n=1, relative_points={'p0': (0, 0)}, color=goal_color,
                 x=goal1_x - 2 * goal_dx, y=goal1_y - 2 * goal_dy, x_dot=0, y_dot=0, draw_radius=goal_r)

    # Define robot fish
    robotfish1 = RobotFish(name='robotfish', num=1, shape='polygon', mass=10, n=6, relative_points={}, color=ball_color,
                           x=fish_x, y=fish_y + fish_dy, x_dot=0, y_dot=0, theta=0)

    # Define pools
    pool1 = Pool(name="pool", num=1, shape='polygon', n=4,
                 relative_points={'p0': (-int(border_x / 2), -width), 'p1': (int(border_x / 2), -width),
                                  'p2': (int(border_x / 2), width), 'p3': (-int(border_x / 2), width)},
                 x=int(border_x / 2), y=-width)

    pool2 = Pool(name="pool", num=1, shape='polygon', n=4,
                 relative_points={'p0': (-width, -int(border_y / 2)), 'p1': (-width, int(border_y / 2)),
                                  'p2': (width, int(border_y / 2)), 'p3': (width, -int(border_y / 2))},
                 x=int(border_x) + width, y=int(border_y / 2))

    pool3 = Pool(name="pool", num=1, shape='polygon', n=4,
                 relative_points={'p0': (-int(border_x / 2), -width), 'p1': (-int(border_x / 2), width),
                                  'p2': (int(border_x / 2), width), 'p3': (int(border_x / 2), -width)},
                 x=int(border_x / 2), y=int(border_y) + width)

    pool4 = Pool(name="pool", num=1, shape='polygon', n=4,
                 relative_points={'p0': (-width, -int(border_x / 2)), 'p1': (-width, int(border_x / 2)),
                                  'p2': (width, int(border_x / 2)), 'p3': (width, -int(border_x / 2))},
                 x=-width, y=int(border_x / 2))


def win():
    """
    Check if a goal is reached by colliding with a ball.
    """
    ab_num = []
    for a in father_obj:
        if a.name == 'goal':
            for b in a.colliding_list:
                if b.name == 'ball':
                    if ab_num.count((a.num, b.num)) == 0:
                        ab_num.append((a.num, b.num))
                        return True
    return False

