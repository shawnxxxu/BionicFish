import math
import util

def central_collision(m1, m2, v1, v2, k):
    """
    Calculate the velocities after a central collision.

    Parameters:
        m1 (float): Mass of the first object
        m2 (float): Mass of the second object
        v1 (float): Velocity of the first object
        v2 (float): Velocity of the second object
        k (float): Coefficient of restitution

    Returns:
        tuple: Velocities after collision for both objects and the impulse magnitude
    """
    _v1 = ((m1 - m2) * v1 + 2 * m2 * v2) / (m1 + m2)
    _v2 = ((m2 - m1) * v2 + 2 * m1 * v1) / (m1 + m2)
    i = m1 * (v1 - _v1) * k
    _v1 = v1 - i / m1
    _v2 = v2 + i / m2
    return _v1, _v2, math.fabs(i)

def non_centric_collision(a, b, dir):
    """
    Handle a non-central collision between two objects.

    Parameters:
        a (object): The first object
        b (object): The second object
        dir (tuple): Direction of the collision force

    Returns:
        float: Impulse magnitude
    """
    theta_d_ba = util.get_theta_of_vector(dir)
    _v_a = util.get_v_final(a.position_colliding[2], a)
    _v_b = util.get_v_final(b.position_colliding[2], b)

    theta_v_a = util.get_theta_of_vector(_v_a)
    theta_v_b = util.get_theta_of_vector(_v_b)
    norm_v_a = util.get_norm_of_vector(_v_a)
    norm_v_b = util.get_norm_of_vector(_v_b)

    _v_a_p = norm_v_a * math.cos(theta_v_a - theta_d_ba)
    _v_b_p = norm_v_b * math.cos(theta_v_b - theta_d_ba)

    v_a_v = norm_v_a * math.sin(theta_v_a - theta_d_ba)
    v_b_v = norm_v_b * math.sin(theta_v_b - theta_d_ba)

    v_a_p, v_b_p, i = central_collision(a.mass, b.mass, _v_a_p, _v_b_p, a.k * b.k)

    dir = util.get_direction_vector(dir)
    vector_dva = util.vector_multiple(dir, i / a.father.mass)
    vector_dvb = util.vector_multiple(dir, -i / b.father.mass)
    a.father.x_dot, a.father.y_dot = util.vector_plus((a.father.x_dot, a.father.y_dot), vector_dva)
    b.father.x_dot, b.father.y_dot = util.vector_plus((b.father.x_dot, b.father.y_dot), vector_dvb)

    a.father.set_v_and_theta_v()
    b.father.set_v_and_theta_v()
    return i

def easy_collision(a, b, dir):
    """
    Handle an easy collision between two objects.

    Parameters:
        a (object): The first object
        b (object): The second object
        dir (tuple): Direction of the collision force
    """
    theta = util.get_theta_of_vector(dir)
    _v_a = util.get_v_of_position_colliding(a)
    theta_v_a = util.get_theta_of_vector(_v_a)
    norm_v_a = util.get_norm_of_vector(_v_a)

    _v_a_p = norm_v_a * math.cos(theta_v_a - theta)
    v_a_v = norm_v_a * math.sin(theta_v_a - theta)

    v_a_p = -_v_a_p * a.k * b.k

    if a.w == 0:
        v_a = (v_a_p, v_a_v)
        a.father.x_dot, a.father.y_dot = util.transform_reference_frame(v_a, -theta)
    else:
        v_a = (v_a_p * a.mass / a.father.mass, v_a_v * a.mass / a.father.mass)
        x_dot, y_dot = util.transform_reference_frame(v_a, -theta)
        a.father.x_dot = a.father.x_dot + x_dot
        a.father.y_dot = a.father.y_dot + y_dot
    a.father.set_v_and_theta_v()

def rotate_after_collision(a, i, vector1, vector2):
    """
    Rotate the object after a collision.

    Parameters:
        a (object): The object to be rotated
        i (float): Impulse magnitude
        vector1 (tuple): Vector from the core to the collision point
        vector2 (tuple): Vector from the core to the collision point on the other object
    """
    min_m = 0
    kk = 1
    theta1 = util.get_theta_of_vector(vector1)
    theta2 = util.get_theta_of_vector(vector2)
    l = math.fabs(util.get_norm_of_vector(vector1) * math.cos(theta1 - theta2))

    if math.fabs(theta1 - theta2) <= math.pi / 2:
        moment_direction = util.bigger_or_smaller(theta1, theta2)
    else:
        moment_direction = util.bigger_or_smaller(theta2, theta1)

    moment = (i * l + min_m) * moment_direction * kk
    a.father.w = a.father.w + moment / a.father.j
