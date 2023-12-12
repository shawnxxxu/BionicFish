import math

def transform_reference_frame(vector, theta):
    x= vector[0] * math.cos(theta) + vector[1] * math.sin(theta)
    y= -vector[0] * math.sin(theta) + vector[1] * math.cos(theta)
    return x,y


def normalize_theta(theta):
    if theta>math.pi:
        return theta-math.pi*2
    elif theta<=-math.pi:
        return theta+math.pi*2
    else:
        return theta

def set_v_and_theta_v(a):
    a.v=math.sqrt(a.x_dot*a.x_dot +a.y_dot*a.y_dot )
    a.theta_v=get_theta_of_vector((a.x_dot , a.y_dot))


def set_x_dot_and_y_dot(a):
    a.x_dot = a.v * math.cos(a.theta_v)
    a.y_dot = a.v * math.sin(a.theta_v)


def vector_plus(vector_a, vector_b):
    return (vector_a[0] + vector_b[0], vector_a[1] + vector_b[1])

def vector_minus(vector_a, vector_b):
    return (vector_a[0] - vector_b[0], vector_a[1] - vector_b[1])

def vector_point_mutiple(vector_a,vector_b):
    return vector_a[0]*vector_b[0]+vector_a[1]*vector_b[1]
def vector_multiple(vector,num):
    _vector=[]
    n=len(vector)
    for i in range(n):
        _vector.append(vector[i]*num)
    return tuple(_vector)




def vector_rotate(vector,theta):
    norm=get_norm_of_vector(vector)
    _theta=get_theta_of_vector(vector)+theta
    return (norm*round(math.cos(_theta),15),norm*round(math.sin(_theta ),15))

def polygon_rotate(realtime_points,point,theta):
    _realtime_points={}
    n=len(realtime_points )
    for i in range(n):
        vector=vector_minus(realtime_points["p%d" % i],point)
        _vector=vector_rotate(vector,theta)
        _realtime_points["p%d" %i]=vector_plus(_vector,point)
    return _realtime_points





def vector_smaller(vector1,vector2):
    if vector1[0]<=vector2[0] and vector1[1]<=vector2[1]:
        return True
    else:
        return False
def vector_bigger(vector1,vector2):
    if vector1[0]>=vector2[0] and vector1[1]>=vector2[1]:
        return True
    else:
        return False


def is_included(vector,range):
    if vector_bigger(vector,range[0])  and vector_smaller(vector ,range[1]) :
        return True
    else:
        return False

def bigger_or_smaller(a,b):
    if a>b:
        return 1
    elif a<b:
        return -1
    else:
        return 0


def get_norm_of_vector(vector):
    "得到向量的模"
    return math.sqrt(vector[0]*vector[0]+vector[1]*vector[1])

def get_direction_vector(vector):
    "得到单位方向向量"
    norm=get_norm_of_vector(vector)
    if norm==0:
        return (0,0)
    else:
        return (vector[0] / norm, vector[1] / norm)


def get_theta_of_vector(value_array):
    """(-pi,pi]"""
    if (value_array[0] < 0 and value_array[1] >= 0):
        theta = math.atan(value_array[1] / value_array[0]) + math.pi
    elif (value_array[0] < 0 and value_array[1] < 0):
        theta = math.atan(value_array[1] / value_array[0]) - math.pi
    elif (value_array[0]==0 and value_array[1]>0):
        theta=math.pi/2
    elif (value_array[0]==0 and value_array[1]<0):
        theta =-math.pi/2
    elif value_array[0]==0 and value_array[1]==0:
        theta=0
    else:
        theta = math.atan(value_array[1] / value_array[0])
    return theta



def get_normal_vector(vector):
    "得到非单位法向量"
    return (vector[1],-vector[0])

def get_theta_between_vectors(vector1,vector2):
    """[0,pi]"""
    if get_norm_of_vector(vector1) * get_norm_of_vector(vector2) == 0:
        return 0
    elif vector_point_mutiple(vector1, vector2) / (get_norm_of_vector(vector1) * get_norm_of_vector(vector2))>1.0 :
        return 0
    elif vector_point_mutiple(vector1, vector2) / (get_norm_of_vector(vector1) * get_norm_of_vector(vector2))<-1.0:
        return math.pi
    else:
        return math.acos(
            vector_point_mutiple(vector1, vector2) / (get_norm_of_vector(vector1) * get_norm_of_vector(vector2)))


def get_vector_from_vector_projection(vector,vector_dir):
    """得到投影向量"""
    theta=get_theta_between_vectors(vector,vector_dir)
    norm=get_norm_of_vector(vector)
    temp=norm*math.cos(theta )
    direction_vector=get_direction_vector(vector_dir)
    return (direction_vector[0]*temp,direction_vector[1]*temp)


def get_distance_between_points(p1,p2,p3):
    k=((p1[0]-p3[0])*(p3[0]-p2[0])+(p1[1]-p3[1])*(p3[1]-p2[1]))/((p2[0]-p3[0])*(p3[0]-p2[0])+(p2[1]-p3[1])*(p3[1]-p2[1]))
    p4=(k*p2[0]+(1-k)*p3[0],k*p2[1]+(1-k)*p3[1])
    distance=get_norm_of_vector(vector_minus(p1,p4) )
    return (k,p4,distance)

def get_direction_of_theta_to_theta(realtime_theta, aiming_theta):
    if math.fabs(aiming_theta -realtime_theta )>=math.pi:
        flag1=1
    else :
        flag1=-1

    if aiming_theta >realtime_theta :
        flag2=1
    elif aiming_theta <realtime_theta :
        flag2=-1
    else:
        flag2=0

    if flag2==0:
        return 0
    else:
        if flag1 == flag2:
            """clockwise"""
            return -1
        else:
            """counterclockwise"""
            return 1



def get_v_of_position_colliding(a):
    v1=(a.father.x_dot,a.father.y_dot)
    r=vector_minus(a.position_colliding[2],(a.father.x,a.father.y))
    v2_temp=get_norm_of_vector(r)*math.fabs(a.father.w)
    if a.father.w==0.0:
        direction=0
    else:
        direction=a.father.w/math.fabs(a.father.w)
    theta_of_v2_temp=normalize_theta(get_theta_of_vector(r)+direction*math.pi/2)
    v2=(v2_temp*math.cos(theta_of_v2_temp ),v2_temp*math.sin(theta_of_v2_temp))
    v=vector_plus(v1,v2)
    if a.father!=a:
        _r=vector_minus(a.position_colliding[2],(a.x,a.y))
        _v2_temp=get_norm_of_vector(_r)*math.fabs(a.w)
        if a.w==0.0:
            _direction=0
        else:
            _direction=a.w/math.fabs(a.w)
        _theta_of_v2_temp=normalize_theta(get_theta_of_vector(_r)+_direction*math.pi/2)
        _v2=(_v2_temp*math.cos(_theta_of_v2_temp ),_v2_temp*math.sin(_theta_of_v2_temp))
        v=vector_plus(v,_v2)


    return v



def get_v_final(vector_pos,a):
    """得到vector_pos对应点的瞬时速度"""
    if a.last==a:
        v=get_v(vector_pos,a)
    else:
        v=vector_plus(get_v(vector_pos,a),get_v(vector_pos,a.last))
    return v
def get_v(vector_pos,a):
    r = vector_minus(vector_pos, (a.x, a.y))
    v_temp = get_norm_of_vector(r) * math.fabs(a.w)
    if a.w==0.0:
        direction=0
    else:
        direction=a.w/math.fabs(a.w)
    theta_of_v_temp = normalize_theta(get_theta_of_vector(r) + direction * math.pi / 2)
    v = (v_temp * math.cos(theta_of_v_temp), v_temp * math.sin(theta_of_v_temp))
    v=vector_plus(v,(a.x_dot,a.y_dot))
    return v
