from util import *

# List containing all objects of the physics class
all_obj = []
# List of objects where the 'father' attribute points to itself
father_obj = []
# List storing circular objects
obj_circle = []
# List storing polygonal objects
obj_polygon = []
# List storing drawable objects
obj_draw = []
# List of objects for collision detection
collision_detection = []
# Dictionary storing objects currently colliding
StillColliding = {}

# Time step for simulation
timestep = 0.03
pre_timestep = 0.02
th = 0
f = -0.8

# Lists for setting parameters of object motion
w_dot_list = [0, 0.6, 0.9, 1.2]
relative_theta_list = [0, 0.2, 0.3, 0.4]
delta_theta_list = [0.1, 0.2, 0.3, 0.4]
tail_waving_list = [1, 2, 3, 4]
tail_waving_direction = 1
v_dot_list = [10, 20, 40, 60]


class physics:
    """
    Class representing physics objects
    """

    def __init__(self, name='debug', num=0, shape='shape', mass=1.0, j=30000, n=0, relative_points={}, radius=0,
                 color=(0, 0, 0), c=None, x=0, y=0, x_dot=0, y_dot=0, theta=0.0, k=0.9, fixed=False, last=None, father=None,
                 draw=True, collision_detection=True, collision_calculation=True, pic_address=None, **kwargs):
        """
        Initializes a physics object.

        :param name: Name
        :param num: Number
        :param shape: Shape
        :param mass: Mass
        :param j: Moment of inertia
        :param n: Number of sides
        :param relative_points: Relative points
        :param radius: Radius
        :param color: Color
        :param c: c
        :param x: x-coordinate
        :param y: y-coordinate
        :param x_dot: x-velocity
        :param y_dot: y-velocity
        :param theta: Rotation angle
        :param k: Restitution coefficient
        :param fixed: Whether it's fixed
        :param last: Previous object
        :param father: Parent object
        :param draw: Whether to draw
        :param collision_detection: Whether to perform collision detection
        :param collision_calculation: Whether to perform collision calculation
        :param pic_address: Image address
        :param kwargs: Additional parameters
        """

        self.name = name
        self.shape = shape
        # mass=0 corresponds to the goal class that does not participate in collision calculation
        self.mass = mass
        # Moment of inertia
        self.j = j
        # Restitution coefficient
        self.k = k
        # Environmental resistance coefficient
        self.f = f
        # Number of sides
        self.n = n
        self.num = num
        self.relative_points = relative_points
        self.radius = radius
        self.color = color
        self.c = c

        self.father = father
        self.son = []
        self.last = last
        self.next = []
        self.set_tree()

        self.fixed = fixed
        self.draw = draw
        self.collision_detection = collision_detection
        self.collision_calculation = collision_calculation

        self.x = x
        self.x_last = x
        self.y = y
        self.y_last = y

        # (-pi, pi]
        self.theta = theta
        self.relative_theta = 0
        self.delta_theta = 0
        self.theta0 = 0
        self.theta_last = theta
        self.realtime_theta = self.get_realtime_theta()
        self.w = 0.0

        self.x_dot = x_dot
        self.y_dot = y_dot
        self.v = get_norm_of_vector((self.x_dot, self.y_dot))
        self.theta_v = get_theta_of_vector((self.x_dot, self.y_dot))

        self.realtime_points = self.get_realtime_points()
        self.position_colliding = None
        self.colliding_list = []
        self.set_list()

        self.pic_address = pic_address

    def set_tree(self):
        """
        Sets the tree structure for objects.
        """
        if self.last == None:
            self.last = self
        else:
            self.last.next.append(self)
        if self.father == None:
            self.father = self
        else:
            self.father.son.append(self)

    def set_list(self):
        """
        Adds the object to various lists based on its properties.
        """
        all_obj.append(self)
        if self.father == self:
            father_obj.append(self)
        if self.draw == True:
            obj_draw.append(self)
        if self.shape == 'polygon':
            obj_polygon.append(self)
        if self.shape == 'circle':
            obj_circle.append(self)
        if self.collision_detection == True:
            collision_detection.append(self)

    def set_relative_edges(self):
        """
        Sets the relative edges of the object based on its relative points.

        :return: A dictionary containing relative edges.
        """
        relative_edges = {}
        for i in range(self.n):
            # Calculate the relative edge vector
            relative_edges["e%d" % i] = vector_minus(self.relative_points["p%d" % ((i + 1) % self.n)],
                                                     self.relative_points["p%d" % (i % self.n)])
        return relative_edges

    def set_relative_normal_edges(self):
        """
        Sets the unit normal vectors for each edge.

        :return: A dictionary containing relative normal edges.
        """
        relative_normal_edges = {}
        for i in range(self.n):
            # Calculate the unit normal vector for each edge
            temp_1 = get_normal_vector(self.relative_edges["e%d" % i])
            temp_2 = self.relative_points["p%d" % i]
            if vector_point_mutiple(temp_1, temp_2) < 0:
                temp_1 = (-temp_1[0], -temp_1[1])
            temp_1 = get_direction_vector(temp_1)
            relative_normal_edges["e%d" % i] = temp_1
        return relative_normal_edges

    def set_range_of_relative_vector_projection_norm(self):
        """
        Returns a dictionary containing the range of projections on unit normal vectors for each edge.

        :return: A dictionary with edge keys and corresponding (min, max) values.
        """
        dict_of_range = {}
        range_of_relative_vector_projection_x = {}
        for i in range(self.n):
            relative_normal_edge = self.relative_normal_edges["e%d" % i]
            for j in range(self.n):
                vector = get_vector_from_vector_projection(self.relative_points["p%d" % j], relative_normal_edge)
                if relative_normal_edge[0] != 0:
                    k = vector[0] / relative_normal_edge[0]
                else:
                    k = vector[1] / relative_normal_edge[1]
                if j == 0:
                    range_of_relative_vector_projection_x["r0"] = k
                elif j == 1:
                    if k < range_of_relative_vector_projection_x["r0"]:
                        range_of_relative_vector_projection_x["r1"] = range_of_relative_vector_projection_x["r0"]
                        range_of_relative_vector_projection_x["r0"] = k
                    elif k >= range_of_relative_vector_projection_x["r0"]:
                        range_of_relative_vector_projection_x["r1"] = k
                elif j >= 2:
                    if k < range_of_relative_vector_projection_x["r0"]:
                        range_of_relative_vector_projection_x["r0"] = k
                    elif k >= range_of_relative_vector_projection_x["r1"]:
                        range_of_relative_vector_projection_x["r1"] = k
            # Save the range of projections for each edge
            dict_of_range["e%d" % i] = (range_of_relative_vector_projection_x["r0"],
                                         range_of_relative_vector_projection_x["r1"])

        return dict_of_range

    def get_realtime_points(self):
        """
        Calculates the real-time points based on rotation and translation.

        :return: A dictionary containing real-time points.
        """
        realtime_points = {}
        for i in range(self.n):
            # Rotate and translate each relative point to get real-time points
            temp = vector_rotate(self.relative_points["p%d" % i], self.get_realtime_theta())
            realtime_points["p%d" % i] = vector_plus(temp, (self.x, self.y))
        return realtime_points

    def get_realtime_theta(self):
        """
        Calculates the real-time rotation angle.

        :return: The real-time rotation angle.
        """
        if self.last == self:
            realtime_theta = self.theta
            return realtime_theta
        else:
            # Sum up rotation angles from the hierarchy
            realtime_theta = self.theta + self.last.realtime_theta + self.relative_theta + self.delta_theta

            return realtime_theta

    def get_realtime_edges(self):
        """
        Calculates the real-time edges based on rotation.

        :return: A dictionary containing real-time edges.
        """
        realtime_edges = {}
        for i in range(self.n):
            # Rotate each relative edge to get real-time edges
            realtime_edges["e%d" % i] = vector_rotate(self.relative_edges["e%d" % i], self.theta)
        return realtime_edges

    def get_realtime_edges(self):
        """
        Calculates the real-time edges based on rotation.

        :return: A dictionary containing real-time edges.
        """
        realtime_edges = {}
        for i in range(self.n):
            # Rotate each relative edge to get real-time edges
            realtime_edges["e%d" % i] = vector_rotate(self.relative_edges["e%d" % i], self.theta)
        return realtime_edges

    def set_v_and_theta_v(self):
        """
        Sets the magnitude and direction of velocity based on x and y components.

        :return: None
        """
        # Calculate the magnitude of velocity
        self.v = math.sqrt(self.x_dot * self.x_dot + self.y_dot * self.y_dot)
        # Calculate the direction of velocity
        self.theta_v = get_theta_of_vector((self.x_dot, self.y_dot))

    def set_x_dot_and_y_dot(self):
        """
        Sets the x and y components of velocity based on magnitude and direction.

        :return: None
        """
        # Calculate the x and y components of velocity
        self.x_dot = self.v * math.cos(self.theta_v)
        self.y_dot = self.v * math.sin(self.theta_v)


class Circle(physics):
    def __init__(self, name, num, shape, mass, n, relative_points, color, x, y, x_dot, y_dot, radius, last=None, father=None):
        """
        Initializes a Circle object.

        :param name: Name
        :param num: Number
        :param shape: Shape
        :param mass: Mass
        :param n: Number of sides
        :param relative_points: Relative points
        :param color: Color
        :param x: x-coordinate
        :param y: y-coordinate
        :param x_dot: x-velocity
        :param y_dot: y-velocity
        :param radius: Radius
        :param last: Previous object
        :param father: Parent object
        """
        physics.__init__(self, name=name, num=num, shape=shape, mass=mass, n=n, relative_points=relative_points,
                         color=color, x=x, y=y, x_dot=x_dot, y_dot=y_dot, last=last, father=father)
        # 'circle' represents the bounding circle
        self.have_circle = False
        self.radius = radius
        # 'core' is the center of the bounding circle
        self.core = (x, y)
        self.j = 200000

    def get_core(self):
        """
        Finds the center of the outer bounding circle.

        :return: The center of the outer bounding circle.
        """
        total = (0, 0)
        for i in range(self.n):
            total = vector_plus(total, self.realtime_points["p%d" % i])
        return (total[0] / self.n, total[1] / self.n)

class goal(Circle):
    """
    Represents a goal object that detects collisions but does not participate in collision calculations.
    """
    def __init__(self, name, num, shape, n, relative_points, color, x, y, x_dot, y_dot, radius=0, mass=0, draw_radius=30):
        """
        Initializes a Goal object.

        :param name: Object name
        :param num: Object number
        :param shape: Object shape
        :param n: Number of sides (for polygons)
        :param relative_points: Relative points for shape
        :param color: Object color
        :param x: x-coordinate
        :param y: y-coordinate
        :param x_dot: x-velocity
        :param y_dot: y-velocity
        :param radius: Object radius (for circles)
        :param mass: Object mass
        :param draw_radius: Radius for drawing purposes
        """
        Circle.__init__(self, name=name, num=num, shape=shape, mass=mass, n=n, relative_points=relative_points,
                         color=color, x=x, y=y, x_dot=x_dot, y_dot=y_dot, radius=radius)
        # Additional properties for goal objects
        self.draw_radius = draw_radius
        self.fixed = True  # Object is fixed and does not move
        self.collision_calculation = False  # Does not participate in collision calculations

class Polygon(physics):
    def __init__(self, name="unnamed", num=0, shape="polygon", mass=99999, j=18000, n=0, relative_points={}, joint_points={},
                 joint_num=None, color=(0, 0, 0), x=0, y=0, x_dot=0.0, y_dot=0.0, theta=0.0, fixed=False, draw=True,
                 collision_detection=True, have_circle=True, collision_calculation=True, last=None, father=None,
                 pic_address=None):
        """
        Initializes a Polygon object.

        :param name: Object name
        :param num: Object number
        :param shape: Object shape
        :param mass: Object mass
        :param j: Rotational inertia
        :param n: Number of sides (for polygons)
        :param relative_points: Relative points for shape
        :param joint_points: Joint points
        :param joint_num: Number of joints
        :param color: Object color
        :param x: x-coordinate
        :param y: y-coordinate
        :param x_dot: x-velocity
        :param y_dot: y-velocity
        :param theta: Rotation angle
        :param fixed: Whether the object is fixed
        :param draw: Whether the object should be drawn
        :param collision_detection: Whether collision detection is enabled
        :param have_circle: Whether the object has a bounding circle
        :param collision_calculation: Whether collision calculation is enabled
        :param last: Previous object in the hierarchy
        :param father: Parent object in the hierarchy
        :param pic_address: Address for an image representation
        """
        physics.__init__(self, name=name, num=num, shape=shape, mass=mass, j=j, n=n, relative_points=relative_points,
                         joint_points=joint_points, joint_num=joint_num, color=color, x=x, y=y, x_dot=x_dot, y_dot=y_dot,
                         theta=theta, fixed=fixed, last=last, father=father, draw=draw,
                         collision_detection=collision_detection, collision_calculation=collision_calculation,
                         pic_address=pic_address)

        self.have_circle = have_circle
        self.relative_edges = self.set_relative_edges()
        self.relative_normal_edges = self.set_relative_normal_edges()
        self.range_of_relative_vector_projection_norm = self.set_range_of_relative_vector_projection_norm()

        self.realtime_edges = self.get_realtime_edges()
        self.realtime_normal_edges = self.get_realtime_normal_edges()

        if self.have_circle:
            self.core = self.get_core()
            self.radius = self.get_radius()

    def set_relative_edges(self):
        """
        Sets the relative edges of the polygon.

        :return: A dictionary containing relative edges.
        """
        relative_edges = {}
        for i in range(self.n):
            relative_edges["e%d" % i] = vector_minus(self.relative_points["p%d" % ((i + 1) % self.n)],
                                                      self.relative_points["p%d" % (i % self.n)])
        return relative_edges

    def set_relative_normal_edges(self):
        """
        Sets the unit normal vectors for each edge.

        :return: A dictionary containing relative normal edges.
        """
        relative_normal_edges = {}
        for i in range(self.n):
            temp_1 = get_normal_vector(self.relative_edges["e%d" % i])
            temp_2 = self.relative_points["p%d" % i]
            if vector_point_mutiple(temp_1, temp_2) < 0:
                temp_1 = (-temp_1[0], -temp_1[1])
            temp_1 = get_direction_vector(temp_1)
            relative_normal_edges["e%d" % i] = temp_1
        return relative_normal_edges

    def get_radius(self):
        """
        Calculates the radius of the bounding circle.

        :return: The radius of the bounding circle.
        """
        r = 0
        for i in range(self.n):
            r_temp = get_norm_of_vector(vector_minus(self.realtime_points["p%d" % i], self.core))
            if r_temp > r:
                r = r_temp
        return r

    def get_core(self):
        """
        Finds the center of the bounding circle.

        :return: The center of the bounding circle.
        """
        total = (0, 0)
        for i in range(self.n):
            total = vector_plus(total, self.realtime_points["p%d" % i])
        return (total[0] / self.n, total[1] / self.n)

    def set_range_of_relative_vector_projection_norm(self):
        """
        Returns a dictionary containing the range of projections on unit normal vectors for each edge.

        :return: A dictionary with edge keys and corresponding (min, max) values.
        """
        dict_of_range = {}
        range_of_relative_vector_projection_x = {}
        for i in range(self.n):
            relative_normal_edge = self.relative_normal_edges["e%d" % i]
            for j in range(self.n):
                vector = get_vector_from_vector_projection(self.relative_points["p%d" % j], relative_normal_edge)
                if relative_normal_edge[0] != 0:
                    k = vector[0] / relative_normal_edge[0]
                else:
                    k = vector[1] / relative_normal_edge[1]
                if j == 0:
                    range_of_relative_vector_projection_x["r0"] = k
                elif j == 1:
                    if k < range_of_relative_vector_projection_x["r0"]:
                        range_of_relative_vector_projection_x["r1"] = range_of_relative_vector_projection_x["r0"]
                        range_of_relative_vector_projection_x["r0"] = k
                    elif k >= range_of_relative_vector_projection_x["r0"]:
                        range_of_relative_vector_projection_x["r1"] = k
                elif j >= 2:
                    if k < range_of_relative_vector_projection_x["r0"]:
                        range_of_relative_vector_projection_x["r0"] = k
                    elif k >= range_of_relative_vector_projection_x["r1"]:
                        range_of_relative_vector_projection_x["r1"] = k
            dict_of_range["e%d" % i] = (range_of_relative_vector_projection_x["r0"],
                                         range_of_relative_vector_projection_x["r1"])
        return dict_of_range

    def get_realtime_points(self):
        """
        Calculates real-time points based on rotation and translation.

        :return: A dictionary containing real-time points.
        """
        realtime_points = {}
        for i in range(self.n):
            temp = vector_rotate(self.relative_points["p%d" % i], self.realtime_theta)
            realtime_points["p%d" % i] = vector_plus(temp, (self.x, self.y))
        return realtime_points

    def get_realtime_edges(self):
        """
        Calculates real-time edges based on rotation.

        :return: A dictionary containing real-time edges.
        """
        realtime_edges = {}
        for i in range(self.n):
            realtime_edges["e%d" % i] = vector_rotate(self.relative_edges["e%d" % i], self.last.theta)
            if self.last != self:
                realtime_edges["e%d" % i] = vector_rotate(self.relative_edges["e%d" % i], self.last.theta + self.theta)
        return realtime_edges

    def get_realtime_normal_edges(self):
        """
        Calculates real-time normal edges based on rotation.

        :return: A dictionary containing real-time normal edges.
        """
        realtime_normal_edges = {}
        for i in range(self.n):
            realtime_normal_edges["e%d" % i] = vector_rotate(self.relative_normal_edges["e%d" % i], self.theta)
            if self.last != self:
                realtime_normal_edges["e%d" % i] = vector_rotate(self.relative_normal_edges["e%d" % i],
                                                                 self.last.theta + self.theta)
        return realtime_normal_edges

class Pool(Polygon):
    def __init__(self, name, num, shape, n, relative_points, x, y):
        """
        Initializes a Pool object(border).

        :param name: Object name
        :param num: Object number
        :param shape: Object shape
        :param n: Number of sides (for polygons)
        :param relative_points: Relative points for shape
        :param x: x-coordinate
        :param y: y-coordinate
        """
        Polygon.__init__(self, name=name, num=num, mass=99999, shape=shape, n=n, x = x, y = y, relative_points=relative_points,
                         have_circle=False)
        self.fixed = True

class RobotFish(Polygon):
    """
    Class representing a robot fish, inheriting from the Polygon class.

    Attributes:
        num (int): Object number.
        name (str): Object name.
        shape (str): Object shape.
        mass (float): Object mass.
        n (int): Number of edges (for polygonal objects).
        relative_points (dict): Dictionary of relative points for polygonal objects.
        color (tuple): RGB color tuple.
        x (float): X-coordinate of the object.
        y (float): Y-coordinate of the object.
        x_dot (float): Velocity in the x-direction.
        y_dot (float): Velocity in the y-direction.
        theta (float): Angle of rotation.
        realtime_theta (float): Real-time angle of rotation.
        last (object): Previous object.
        next (list): List of next objects.
        son (list): List of child objects.
        w_dot_list (list): List of angular acceleration values affecting fish rotation.
        w_dot_direction (int): Direction of angular acceleration.
        w_dot_number (int): Index of angular acceleration value.
        w_mode (int): Mode controlling the choice of angular acceleration value.
        w_dot (float): Angular acceleration value for fish rotation.
        relative_theta_list (list): List of relative swing angles for fish tail.
        tail_waving_list (list): List of tail waving speeds.
        tail_waving_direction (int): Direction of tail waving.
        v_dot_list (list): List of acceleration values affecting fish swimming speed.
        v_mode (int): Mode controlling the choice of acceleration value for swimming.
        v_dot (float): Acceleration value for fish swimming.
        delta_theta_list (list): List of lag swing angles for the fish.
        _next (list): Temporary storage for the 'next' attribute.
        _son (list): Temporary storage for the 'son' attribute.
        relative_points (dict): Updated relative points for the polygonal object.
        have_circle (bool): Flag indicating if the fish has a circular core.
        radius (float): Radius of the circular core.
        core (tuple): Coordinates of the circular core.
        j (float): Moment of inertia.
    """

    def __init__(self, num, name, shape, mass, n, relative_points, color, x, y, x_dot, y_dot, theta):
        # Initialization of attributes specific to RobotFish
        self.realtime_theta = theta
        self.theta = theta
        self.last = self
        self.next = []
        self.son = []
        self.set_robotfish(num, x, y)

        # Attributes controlling fish rotation
        self.w_dot_list = w_dot_list
        self.w_dot_direction = 1
        self.w_dot_number = 0
        self.w_mode = 0
        self.w_dot = self.w_dot_list[self.w_mode]

        # Attributes controlling fish tail waving
        self.relative_theta_list = relative_theta_list

        # Attributes controlling tail waving speed
        self.tail_waving_list = tail_waving_list
        self.tail_waving_direction = 1

        # Attributes controlling fish swimming speed
        self.v_dot_list = v_dot_list
        self.v_mode = 0
        self.v_dot = self.v_dot_list[self.v_mode]

        # Attributes controlling lag swing angles
        self.delta_theta_list = delta_theta_list

        # Additional attributes related to fish properties
        self.realtime_theta = self.get_realtime_theta()
        self._next = self.next
        self._son = self.son
        self.relative_points = self.get_relative_points()

        # Call to the parent class constructor (Polygon)
        Polygon.__init__(self, name=name, num=num, shape=shape, mass=mass, n=n, relative_points=self.relative_points,
                         color=color, x=x, y=y, x_dot=x_dot, y_dot=y_dot, theta=theta, draw=False, collision_detection=True)

        # Restore the temporarily stored 'next' and 'son' attributes
        self.next = self._next
        self.son = self._son

        # Check if the fish has a circular core
        self.have_circle = True
        if self.have_circle:
            self.radius = self.get_radius()
            self.core = self.get_core()

        # Set the moment of inertia
        self.j = 30000

    def set_robotfish(self, num, x, y):
        """
        Set up the components of the robot fish.

        Parameters:
            num (int): Object number.
            x (float): X-coordinate of the robot fish.
            y (float): Y-coordinate of the robot fish.
        """
        # Define the fish head as a circular component
        self.fish_head = Circle("fish_head", num, 'circle', mass=10, n=1, relative_points={'p0': (20, 0)}, radius=10,
                                x=0, y=0, x_dot=0, y_dot=0, color=(20, 120, 200), last=self, father=self)

        # Define the fish body components as polygonal shapes
        self.fish_body1 = Polygon("fish_body1", num, 'polygon', mass=10, n=4,
                                  relative_points={'p0': (20, 10), 'p1': (-10, 10), 'p2': (-10, -10), 'p3': (20, -10)},
                                  color=(20, 120, 200), x=x, y=y, theta=0, collision_detection=True,
                                  last=self, father=self)

        self.fish_body2 = Polygon("fish_body2", num, 'polygon', mass=0.4, n=4,
                                  relative_points={'p0': (0, 10), 'p1': (-20, 5), 'p2': (-20, -5), 'p3': (0, -10)},
                                  color=(20, 120, 200), x=-10 + x, y=y, theta=0, collision_detection=True,
                                  last=self, father=self)

        self.fish_body3 = Polygon("fish_body3", num, 'polygon', mass=0.4, n=3,
                                  relative_points={'p0': (0, 5), 'p1': (-20, 0), 'p2': (0, -5)}, color=(20, 120, 200),
                                  x=-40 + x, y=y, theta=0, collision_detection=True,
                                  last=self.fish_body2, father=self)

        self.fish_tail = Polygon("fish_tail", num, 'polygon', mass=0.4, n=3,
                                 relative_points={'p0': (0, 0), 'p1': (-20, 2), 'p2': (-20, -2)}, color=(20, 120, 200),
                                 theta=0, collision_detection=True,
                                 last=self.fish_body3, father=self)

        # List of robot fish components
        self.robotfish_list = [self.fish_head, self.fish_body1, self.fish_body2, self.fish_body3, self.fish_tail]

    def get_core(self):
        """
        Calculate the center coordinates of the circular core.

        Returns:
            tuple: Coordinates of the circular core.
        """
        return vector_multiple(vector_plus(self.realtime_points['p2'], self.realtime_points['p4']), 0.5)

    def get_radius(self):
        """
        Get the radius of the circular core.

        Returns:
            float: Radius of the circular core.
        """
        r = 61
        return r

    def get_relative_points(self):
        """
        Get the relative points of the robot fish.

        Returns:
            dict: Dictionary of relative points.
        """
        _dict = {'p0': self.fish_head.relative_points['p0'],
                 'p1': self.fish_body1.relative_points['p0'],
                 'p2': self.fish_body1.relative_points['p1'],
                 'p3': self.fish_body2.relative_points['p1'],
                 'p4': self.fish_body1.relative_points['p2'],
                 'p5': self.fish_body1.relative_points['p3']}
        return _dict

    def fish_body2_update(self):
        """
        Update the position and real-time theta of fish_body2.
        """
        a = self.fish_body2
        # Update position based on midpoint of fish_body1's edge
        (a.x, a.y) = vector_multiple(vector_plus(self.fish_body1.realtime_points['p1'], self.fish_body1.realtime_points['p2']), 0.5)
        a.realtime_theta = a.theta + a.last.realtime_theta

    def fish_tail_update(self):
        """
        Update the position and real-time theta of fish_tail.
        """
        a = self.fish_tail
        # Update position based on fish_body2's edge
        (a.x, a.y) = self.fish_body2.realtime_points['p1']
        a.realtime_theta = a.theta + a.last.realtime_theta

    def update(self):
        """
        Update the position and real-time properties of all robot fish components.
        """
        for a in self.robotfish_list:
            (a.x, a.y) = (self.x, self.y)
            if a == self.fish_body2:
                self.fish_body2_update()
            elif a == self.fish_body3:
                # Update position based on midpoint of fish_body2's edge
                (a.x, a.y) = vector_multiple(vector_plus(self.fish_body2.realtime_points['p1'], self.fish_body2.realtime_points['p2']), 0.5)
                a.relative_theta = self.relative_theta_list[self.w_mode] * self.w_dot_direction * -1
            elif a == self.fish_tail:
                # Update position based on fish_body3's edge
                (a.x, a.y) = self.fish_body3.realtime_points['p1']
                a.relative_theta = self.relative_theta_list[self.w_mode] * self.w_dot_direction * -1

            # Update position based on fish_body3's edge
            a.realtime_theta = a.get_realtime_theta()
            a.realtime_points = a.get_realtime_points()
            a.core = a.get_core()

    def wave_tail(self):
        """
        Implement tail waving motion for the robot fish.
        """
        max_theta = 0.5
        for a in self.robotfish_list:
            if a == self.fish_body2:
                # Check and adjust direction of tail waving
                if a.theta > max_theta:
                    self.tail_waving_direction = -1
                if a.theta < -max_theta:
                    self.tail_waving_direction = 1
                # Set angular velocity for tail waving
                a.w = self.tail_waving_list[self.v_mode] * self.tail_waving_direction
                # Update theta based on angular velocity
                a.theta = a.theta + a.w * timestep
            elif a == self.fish_body3:
                # Set angular velocity for tail waving
                a.delta_theta = -self.delta_theta_list[self.w_mode] * self.w_dot_direction
                # Check and adjust direction of tail waving
                if a.theta + a.delta_theta > max_theta:
                    self.tail_waving_direction = -1
                if a.theta + a.delta_theta < -max_theta:
                    self.tail_waving_direction = 1
                # Set angular velocity for tail waving
                a.w = self.tail_waving_list[self.v_mode] * self.tail_waving_direction
            elif a == self.fish_tail:
                # Set angular velocity for tail waving
                a.delta_theta = -self.delta_theta_list[self.w_mode] * self.w_dot_direction
                # Check and adjust direction of tail waving
                if a.theta + a.delta_theta > max_theta:
                    self.tail_waving_direction = -1
                if a.theta + a.delta_theta < -max_theta:
                    self.tail_waving_direction = 1
                # Set angular velocity for tail waving
                a.w = self.tail_waving_list[self.v_mode] * self.tail_waving_direction
