import math

def normalize_theta(theta):
    """
    Normalize an angle to be within the range [-pi, pi).

    Parameters:
        theta (float): Input angle

    Returns:
        float: Normalized angle
    """
    if theta > math.pi:
        return theta - math.pi * 2
    elif theta <= -math.pi:
        return theta + math.pi * 2
    else:
        return theta


def vector_plus(vector_a, vector_b):
    """
    Add two vectors element-wise.

    Parameters:
        vector_a (tuple): First vector (a1, a2)
        vector_b (tuple): Second vector (b1, b2)

    Returns:
        tuple: Resultant vector (a1 + b1, a2 + b2)
    """
    return (vector_a[0] + vector_b[0], vector_a[1] + vector_b[1])

def vector_minus(vector_a, vector_b):
    """
    Subtract vector_b from vector_a element-wise.

    Parameters:
        vector_a (tuple): First vector (a1, a2)
        vector_b (tuple): Second vector (b1, b2)

    Returns:
        tuple: Resultant vector (a1 - b1, a2 - b2)
    """
    return (vector_a[0] - vector_b[0], vector_a[1] - vector_b[1])

def vector_point_mutiple(vector_a, vector_b):
    """
    Calculate the dot product of two vectors.

    Parameters:
        vector_a (tuple): First vector (a1, a2)
        vector_b (tuple): Second vector (b1, b2)

    Returns:
        float: Dot product of the two vectors (a1 * b1 + a2 * b2)
    """
    return vector_a[0] * vector_b[0] + vector_a[1] * vector_b[1]

def vector_multiple(vector, num):
    """
    Multiply each element of a vector by a scalar.

    Parameters:
        vector (tuple): Input vector
        num (float): Scalar multiplier

    Returns:
        tuple: Resultant vector after multiplication
    """
    _vector = []
    n = len(vector)
    for i in range(n):
        _vector.append(vector[i] * num)
    return tuple(_vector)

def vector_rotate(vector, theta):
    """
    Rotate a 2D vector by a specified angle.

    Parameters:
        vector (tuple): Input vector (x, y)
        theta (float): Angle of rotation

    Returns:
        tuple: Rotated vector (x', y')
    """
    norm = get_norm_of_vector(vector)
    _theta = get_theta_of_vector(vector) + theta
    return (norm * round(math.cos(_theta), 15), norm * round(math.sin(_theta), 15))



def get_norm_of_vector(vector):
    """
    Calculate the Euclidean norm (magnitude) of a 2D vector.

    Parameters:
        vector (tuple): Input vector (x, y)

    Returns:
        float: Euclidean norm of the vector
    """
    return math.sqrt(vector[0] * vector[0] + vector[1] * vector[1])


def get_direction_vector(vector):
    """
    Calculate the unit direction vector of a 2D vector.

    Parameters:
        vector (tuple): Input vector (x, y)

    Returns:
        tuple: Unit direction vector (x_normalized, y_normalized)
    """
    norm = get_norm_of_vector(vector)
    if norm == 0:
        return (0, 0)
    else:
        return (vector[0] / norm, vector[1] / norm)


def get_theta_of_vector(value_array):
    """
    Calculate the polar angle (theta) of a 2D vector in the range (-pi, pi].

    Parameters:
        value_array (tuple): Input vector (x, y)

    Returns:
        float: Polar angle (theta) of the vector
    """
    if value_array[0] < 0 and value_array[1] >= 0:
        theta = math.atan(value_array[1] / value_array[0]) + math.pi
    elif value_array[0] < 0 and value_array[1] < 0:
        theta = math.atan(value_array[1] / value_array[0]) - math.pi
    elif value_array[0] == 0 and value_array[1] > 0:
        theta = math.pi / 2
    elif value_array[0] == 0 and value_array[1] < 0:
        theta = -math.pi / 2
    elif value_array[0] == 0 and value_array[1] == 0:
        theta = 0
    else:
        theta = math.atan(value_array[1] / value_array[0])
    return theta

def bigger_or_smaller(a, b):
    """
    Compare two values and return 1 if a > b, -1 if a < b, and 0 if a == b.

    Parameters:
        a: First value
        b: Second value

    Returns:
        int: 1 if a > b, -1 if a < b, 0 if a == b
    """
    if a > b:
        return 1
    elif a < b:
        return -1
    else:
        return 0

def get_normal_vector(vector):
    """
    Get the non-unit normal vector (perpendicular) to the input vector.

    Parameters:
        vector (tuple): Input vector (x, y)

    Returns:
        tuple: Non-unit normal vector (y, -x)
    """
    return (vector[1], -vector[0])


def get_theta_between_vectors(vector1, vector2):
    """
    Get the angle (theta) between two vectors in the range [0, pi].

    Parameters:
        vector1 (tuple): First vector (x1, y1)
        vector2 (tuple): Second vector (x2, y2)

    Returns:
        float: Angle (theta) between the vectors
    """
    if get_norm_of_vector(vector1) * get_norm_of_vector(vector2) == 0:
        return 0
    elif (
        vector_point_mutiple(vector1, vector2)
        / (get_norm_of_vector(vector1) * get_norm_of_vector(vector2))
        > 1.0
    ):
        return 0
    elif (
        vector_point_mutiple(vector1, vector2)
        / (get_norm_of_vector(vector1) * get_norm_of_vector(vector2))
        < -1.0
    ):
        return math.pi
    else:
        return math.acos(
            vector_point_mutiple(vector1, vector2)
            / (get_norm_of_vector(vector1) * get_norm_of_vector(vector2))
        )


def get_vector_from_vector_projection(vector, vector_dir):
    """
    Get the vector projection of 'vector' onto 'vector_dir'.

    Parameters:
        vector (tuple): Input vector (x, y)
        vector_dir (tuple): Direction vector for projection (x_dir, y_dir)

    Returns:
        tuple: Vector projection of 'vector' onto 'vector_dir'
    """
    theta = get_theta_between_vectors(vector, vector_dir)
    norm = get_norm_of_vector(vector)
    temp = norm * math.cos(theta)
    direction_vector = get_direction_vector(vector_dir)
    return (direction_vector[0] * temp, direction_vector[1] * temp)


def get_distance_between_points(p1, p2, p3):
    """
    Get the distance between a point 'p1' and the line segment formed by 'p2' and 'p3'.

    Parameters:
        p1 (tuple): Point coordinates (x1, y1)
        p2 (tuple): Line segment endpoint coordinates (x2, y2)
        p3 (tuple): Line segment endpoint coordinates (x3, y3)

    Returns:
        tuple: Tuple containing the parameter 'k', the closest point 'p4' on the line segment,
               and the distance between 'p1' and 'p4'.
    """
    k = (
        (p1[0] - p3[0]) * (p3[0] - p2[0]) + (p1[1] - p3[1]) * (p3[1] - p2[1])
    ) / ((p2[0] - p3[0]) * (p3[0] - p2[0]) + (p2[1] - p3[1]) * (p3[1] - p2[1]))
    p4 = (k * p2[0] + (1 - k) * p3[0], k * p2[1] + (1 - k) * p3[1])
    distance = get_norm_of_vector(vector_minus(p1, p4))
    return (k, p4, distance)


def get_direction_of_theta_to_theta(realtime_theta, aiming_theta):
    """
    Get the direction (clockwise, counterclockwise, or none) from 'realtime_theta' to 'aiming_theta'.

    Parameters:
        realtime_theta (float): Current angle in radians
        aiming_theta (float): Target angle in radians

    Returns:
        int: 0 for no change, -1 for clockwise, 1 for counterclockwise
    """
    if math.fabs(aiming_theta - realtime_theta) >= math.pi:
        flag1 = 1
    else:
        flag1 = -1

    if aiming_theta > realtime_theta:
        flag2 = 1
    elif aiming_theta < realtime_theta:
        flag2 = -1
    else:
        flag2 = 0

    if flag2 == 0:
        return 0
    else:
        if flag1 == flag2:
            # clockwise
            return -1
        else:
            # counterclockwise
            return 1


def get_v_final(vector_pos, a):
    """
    Get the instantaneous velocity at a given position for the combined object.

    Parameters:
        vector_pos (tuple): Position vector (x, y)
        a: Object for which velocity is calculated

    Returns:
        tuple: Instantaneous velocity vector at the position
    """
    if a.last == a:
        v = get_v(vector_pos, a)
    else:
        v = vector_plus(get_v(vector_pos, a), get_v(vector_pos, a.last))
    return v


def get_v(vector_pos, a):
    """
    Get the instantaneous velocity at a given position for the individual object.

    Parameters:
        vector_pos (tuple): Position vector (x, y)
        a: Object for which velocity is calculated

    Returns:
        tuple: Instantaneous velocity vector at the position
    """
    r = vector_minus(vector_pos, (a.x, a.y))
    v_temp = get_norm_of_vector(r) * math.fabs(a.w)
    if a.w == 0.0:
        direction = 0
    else:
        direction = a.w / math.fabs(a.w)
    theta_of_v_temp = normalize_theta(get_theta_of_vector(r) + direction * math.pi / 2)
    v = (v_temp * math.cos(theta_of_v_temp), v_temp * math.sin(theta_of_v_temp))
    v = vector_plus(v, (a.x_dot, a.y_dot))
    return v

