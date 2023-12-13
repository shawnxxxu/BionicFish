import math
import util
import function

# Global variable for collision range
global C_RANGE
C_RANGE = 0

def final_is_colliding(a, b, a_flag=0, b_flag=0):
    """
    Check if two objects are colliding and return the collision result along with object information.

    Parameters:
        a (object): The first object
        b (object): The second object
        a_flag (int): Flag for the first object, default is 0
        b_flag (int): Flag for the second object, default is 0

    Returns:
        bool: Whether a collision occurred
        object: The first object involved in the collision
        object: The second object involved in the collision
    """
    # Check if collision detection is enabled for both objects
    if a.collision_detection and b.collision_detection:
        # Determine the shape of the first object
        if a.have_circle and a_flag == 0:
            a_shape = "circle"
            a_flag = 1
        else:
            a_shape = a.shape
            a_flag = 0

        # Determine the shape of the second object
        if b.have_circle and b_flag == 0:
            b_shape = "circle"
            b_flag = 1
        else:
            b_shape = b.shape
            b_flag = 0

        # Check if the objects are colliding
        a_b_iscolliding = is_colliding(a, b, a_shape, b_shape)

        if not a_b_iscolliding:
            return False

        # If there are no child objects
        if a.son == [] and b.son == []:
            if a_flag == 0 and b_flag == 0:
                # Add colliding objects to each other's colliding lists
                a.father.colliding_list.append(b.father)
                b.father.colliding_list.append(a.father)

                # Handle specific collision cases
                if a.shape == "polygon" and b.shape == "circle":
                    if is_v_v(a_b_iscolliding[1][2], b, a, a_b_iscolliding[3]):
                        a.position_colliding = a_b_iscolliding[2]
                        b.position_colliding = a_b_iscolliding[1]
                        print(b.name, a.name, "is colliding and calculated")
                        return True, b, a
                else:
                    if is_v_v(a_b_iscolliding[1][2], a, b, a_b_iscolliding[3]):
                        a.position_colliding = a_b_iscolliding[1]
                        b.position_colliding = a_b_iscolliding[2]
                        print(a.name, b.name, "is colliding and calculated")
                        return True, a, b
            else:
                # Recursive call for further checking
                return final_is_colliding(a, b, a_flag, b_flag)

            return False
        else:
            # If there are child objects, check collisions recursively
            if a.son != []:
                for i in a.son:
                    if b.son != []:
                        for j in b.son:
                            i_j_iscolliding = final_is_colliding(i, j)
                            if i_j_iscolliding:
                                return True, i, j
                    else:
                        i_b_iscolliding = final_is_colliding(i, b)
                        if i_b_iscolliding:
                            return True, i, b
            else:
                for j in b.son:
                    j_a_iscolliding = final_is_colliding(j, a)
                    if j_a_iscolliding:
                        return True, j, a

            return False

    return False



def is_colliding(a, b, a_shape, b_shape):
    """
    Check if two objects are colliding based on their shapes and return the collision result.

    Parameters:
        a (object): The first object
        b (object): The second object
        a_shape (str): The shape of the first object ("circle" or "polygon")
        b_shape (str): The shape of the second object ("circle" or "polygon")

    Returns:
        bool: Whether a collision occurred
    """
    # Initialize position_colliding attributes to None
    a.position_colliding = None
    b.position_colliding = None

    # Determine the collision based on the shapes of the objects
    if a_shape == "circle" and b_shape == "circle":
        is_colliding = is_colliding_c_c(a, b)
    elif a_shape == "circle" and b_shape == "polygon":
        is_colliding = is_colliding_c_p(a, b)
    elif a_shape == "polygon" and b_shape == "circle":
        is_colliding = is_colliding_c_p(b, a)
    elif a_shape == "polygon" and b_shape == "polygon":
        is_colliding = is_colliding_p_p(a, b)

    return is_colliding


def is_colliding_c_c(a, b):
    """
    Check if two circle objects are colliding and return the collision result.

    Parameters:
        a (object): The first circle object
        b (object): The second circle object

    Returns:
        bool: Whether a collision occurred
        tuple: Information about the collision on the first circle
        tuple: Information about the collision on the second circle
        tuple: Normal vector of the collision
    """
    # Calculate the sum of radii
    radius = a.radius + b.radius

    # Calculate the distance between the centers of the circles
    distance = util.get_norm_of_vector(util.vector_minus(a.core, b.core))

    # Check if the distance is less than or equal to the sum of radii plus a range (C_RANGE)
    if distance <= radius + C_RANGE:
        # Calculate the normal vector pointing from the second circle to the first
        n_ab = util.vector_minus(b.core, a.core)

        # Calculate the position of the collision on the edge of the first circle
        pos_a = util.vector_plus(a.core, util.vector_multiple(n_ab, a.radius / radius))

        # Calculate the position of the collision on the edge of the second circle
        pos_b = util.vector_plus(b.core, util.vector_multiple(n_ab, -b.radius / radius))

        # Return True to indicate a collision and provide collision information
        return True, ("edge", 0, pos_a), ("edge", 0, pos_b), n_ab

    # Return False if no collision occurred
    return False

def is_colliding_c_p(a, b):
    """
    Check if a circle and a polygon are colliding and return the collision result.

    Parameters:
        a (object): The circle object
        b (object): The polygon object

    Returns:
        bool: Whether a collision occurred
        tuple: Information about the collision on the circle
        tuple: Information about the collision on the polygon
        tuple: Normal vector of the collision
    """
    # Obtain real-time information about edges and points of the polygon
    dict_points_b = b.get_realtime_points()

    # Initialize position_colliding attributes to None
    a_position_colliding = None
    b_position_colliding = None

    POINT_COLLIDING = False

    # Check for collision with each point of the polygon
    for i1 in range(b.n):
        if util.get_norm_of_vector(util.vector_minus(a.core, dict_points_b["p%d" % i1])) <= a.radius + C_RANGE:
            b_position_colliding = ("point", i1, dict_points_b["p%d" % i1])
            a_position_colliding = ("edge", 0, dict_points_b["p%d" % i1])
            POINT_COLLIDING = True
            break
        else:
            POINT_COLLIDING = False

    # If no collision with points, check for collision with edges
    if not POINT_COLLIDING:
        for i2 in range(b.n):
            _vector = util.get_distance_between_points(a.core, dict_points_b["p%d" % i2],
                                                       dict_points_b["p%d" % ((i2 + 1) % b.n)])
            if _vector[2] <= a.radius + C_RANGE:
                if 0 <= _vector[0] <= 1:
                    b_position_colliding = ("edge", i2, _vector[1])
                    a_position_colliding = ("edge", 0, _vector[1])
                    break

    # If a collision occurred, calculate the normal vector and position
    if a_position_colliding is not None:
        n_ab = util.vector_minus(a_position_colliding[2], a.core)
        return True, a_position_colliding, b_position_colliding, n_ab

    # Return False if no collision occurred
    return False

def is_colliding_p_p(a, b):
    """
    Check if two polygons are colliding and return the collision result.

    Parameters:
        a (object): The first polygon object
        b (object): The second polygon object

    Returns:
        bool: Whether a collision occurred
        tuple: Information about the collision on the first polygon
        tuple: Information about the collision on the second polygon
        tuple: Normal vector of the collision
    """
    # Obtain real-time information about points, ranges, and normal edges of both polygons
    dict_points_a = a.get_realtime_points()
    dict_points_b = b.get_realtime_points()
    dict_of_range_b = b.range_of_relative_vector_projection_norm
    dict_of_range_a = a.range_of_relative_vector_projection_norm
    realtime_normal_edges_a = a.get_realtime_normal_edges()
    realtime_normal_edges_b = b.get_realtime_normal_edges()

    # Initialize position_colliding attributes to None
    a_position_colliding = None
    b_position_colliding = None

    for i in range(a.n):
        # Check if a point from polygon A is inside polygon B
        flag = 0
        relative_vector_ab = util.vector_minus(dict_points_a["p%d" % i], (b.x, b.y))

        for j in range(b.n):
            vector = util.get_vector_from_vector_projection(relative_vector_ab, realtime_normal_edges_b["e%d" % j])

            if realtime_normal_edges_b["e%d" % j][0] != 0:
                k = vector[0] / realtime_normal_edges_b["e%d" % j][0]
            else:
                k = vector[1] / realtime_normal_edges_b["e%d" % j][1]

            # Check if the point is within the specified range along the edge
            if k < dict_of_range_b["e%d" % j][0] or k > dict_of_range_b["e%d" % j][1]:
                flag = 1
                break
            else:
                temp1 = math.fabs(k - dict_of_range_b["e%d" % j][0])
                temp2 = math.fabs(k - dict_of_range_b["e%d" % j][1])

                if temp2 < temp1:
                    temp1 = temp2

                if j == 0:
                    temp = temp1
                    num = j
                else:
                    if temp1 < temp:
                        temp = temp1
                        num = j

        if flag == 0:
            point = dict_points_a["p%d" % i]
            a_position_colliding = ("point", i, point)
            b_position_colliding = ("edge", num, point)
            n_ab = util.vector_multiple(realtime_normal_edges_b["e%d" % num], -1)
            break

    for i in range(b.n):
        # Check if a point from polygon B is inside polygon A
        flag = 0
        relative_vector_ba = util.vector_minus(dict_points_b["p%d" % i], (a.x, a.y))

        for j in range(a.n):
            vector = util.get_vector_from_vector_projection(relative_vector_ba, realtime_normal_edges_a["e%d" % j])

            if realtime_normal_edges_a["e%d" % j][0] != 0:
                k = vector[0] / realtime_normal_edges_a["e%d" % j][0]
            else:
                k = vector[1] / realtime_normal_edges_a["e%d" % j][1]

            # Check if the point is within the specified range along the edge
            if k < dict_of_range_a["e%d" % j][0] or k > dict_of_range_a["e%d" % j][1]:
                flag = 1
                break
            else:
                temp1 = math.fabs(k - dict_of_range_a["e%d" % j][0])
                temp2 = math.fabs(k - dict_of_range_a["e%d" % j][1])

                if temp2 < temp1:
                    temp1 = temp2

                if j == 0:
                    temp = temp1
                    num = j
                else:
                    if temp1 < temp:
                        temp = temp1
                        num = j

        if flag == 0:
            point = dict_points_b["p%d" % i]
            b_position_colliding = ("point", i, point)
            a_position_colliding = ("edge", num, point)
            n_ab = realtime_normal_edges_a["e%d" % num]
            break

    # If a collision occurred, return True along with collision information
    if a_position_colliding is not None:
        return True, a_position_colliding, b_position_colliding, n_ab

    # Return False if no collision occurred
    return False



def is_v_v(pos, a, b, n_ab):
    """
    Check if the collision point velocities are in the "mutually approaching" state.

    Parameters:
        pos (tuple): The collision point position
        a (object): The first object
        b (object): The second object
        n_ab (tuple): Normal vector of the collision

    Returns:
        bool: Whether the velocities are in the "mutually approaching" state
    """
    # Get final velocities at the collision point for both objects
    v_a = util.get_v_final(pos, a)
    v_b = util.get_v_final(pos, b)

    # Calculate the relative velocity at the collision point
    v_ab = util.vector_minus(v_a, v_b)

    # Check if the relative velocity is in the direction of the normal vector
    if util.vector_point_mutiple(v_ab, n_ab) > float(0):
        return True
    else:
        return False


def AfterCollision(a, b):
    """
    Handle actions after a collision between two objects.

    Parameters:
        a (object): The first object involved in the collision
        b (object): The second object involved in the collision
    """
    # Check if a is a fish tail or fish body, and update tail waving direction
    if a.name == "fish_tail" or a.name == "fish_body2":
        a.father.tail_waving_direction = -a.father.tail_waving_direction

    # Check if b is a fish tail or fish body, and update tail waving direction
    if b.name == "fish_tail" or b.name == "fish_body2":
        b.father.tail_waving_direction = -b.father.tail_waving_direction

    print(a.name, b.name, 'is AfterCollision')

    # Check if both objects are fixed
    if a.fixed and b.fixed:
        pass

    # Check if only b is fixed
    elif b.fixed and not a.fixed:
        if b.shape == "polygon":
            if a.shape == "circle":
                dict_normal_edge = b.get_realtime_normal_edges()
                d = dict_normal_edge["e%d" % b.position_colliding[1]]
                i = function.non_centric_collision(a, b, d)
            elif a.shape == "polygon":
                if a.position_colliding[0] == "edge" and b.position_colliding[0] == "point":
                    dict_normal_edge = a.get_realtime_normal_edges()
                    d = dict_normal_edge["e%d" % a.position_colliding[1]]
                    d = util.vector_multiple(d, -1)
                elif b.position_colliding[0] == "edge" and a.position_colliding[0] == "point":
                    dict_normal_edge = b.get_realtime_normal_edges()
                    d = dict_normal_edge["e%d" % b.position_colliding[1]]
                i = function.non_centric_collision(a, b, d)

            vector1 = util.vector_minus(a.position_colliding[2], (a.x, a.y))
            function.rotate_after_collision(a, i, vector1, d)
            b.x_dot, b.y_dot, b.v, b.v_theta = (0, 0, 0, 0)

    # Check if both objects are not fixed
    elif not a.fixed and not b.fixed:
        # Handle collision between two circles
        if a.shape == "circle" and b.shape == "circle":
            x_ba = a.x - b.x
            y_ba = a.y - b.y
            d = (x_ba, y_ba)
            i = function.non_centric_collision(a, b, d)

        # Handle collision between a circle and a polygon
        elif a.shape == "circle" and b.shape == "polygon":
            colliding_type = b.position_colliding[0]
            colliding_position = b.position_colliding[2]
            if colliding_type == "point":
                x_ba = a.x - colliding_position[0]
                y_ba = a.y - colliding_position[1]
                d = (x_ba, y_ba)
                i = function.non_centric_collision(a, b, d)
            else:
                colliding_edge = b.position_colliding[1]
                dict_normal_vector = b.get_realtime_normal_edges()
                d = dict_normal_vector["e%d" % colliding_edge]
                i = function.non_centric_collision(a, b, d)

            vector1 = util.vector_minus(colliding_position, (b.x, b.y))
            function.rotate_after_collision(b, i, vector1, d)

        # Handle collision between two polygons
        elif a.shape == "polygon" and b.shape == "polygon":
            colliding_position = a.position_colliding[2]
            if a.position_colliding[0] == "edge" and b.position_colliding[0] == "point":
                dict_normal_edge = a.get_realtime_normal_edges()
                d = dict_normal_edge["e%d" % a.position_colliding[1]]
                d = util.vector_multiple(d, -1)
            else:
                dict_normal_edge = b.get_realtime_normal_edges()
                d = dict_normal_edge["e%d" % b.position_colliding[1]]

            i = function.non_centric_collision(a, b, d)
            vector1 = util.vector_minus(colliding_position, (a.x, a.y))
            function.rotate_after_collision(a, i, vector1, d)
            vector2 = util.vector_minus(colliding_position, (b.x, b.y))
            function.rotate_after_collision(b, i, vector2, d)

    return None
