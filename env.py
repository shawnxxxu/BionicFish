from util import *

"包含所有physics类"
all_obj=[]
"self.father==self"
father_obj=[]
obj_circle = []
obj_polygon=[]
obj_draw=[]
collision_detection = []
_collision_detection=[]
"""collision_calculation=[]
"""
StillColliding={}


timestep = 0.03
pre_timestep=0.02
th=0
f=-0.8

w_dot_list = [0, 0.6, 0.9, 1.2]
relative_theta_list = [0, 0.2, 0.3, 0.4]
delta_theta_list=[0.1,0.2,0.3,0.4]
tail_waving_list = [1, 2, 3, 4]
tail_waving_direction = 1
v_dot_list=[10,20,40,60]



class physics():
    def __init__(self, name='debug', num=0,shape='shape', mass=1.0, j=30000,n=0,relative_points={},radius=0,color=(0, 0, 0),c=None, x=0, y=0, x_dot=0, y_dot=0, theta=0.0, k=0.9,fixed=False, last=None, father=None ,draw=True, collision_detection=True, collision_calculation=True,pic_address=None,**kwag):
        self.name=name
        self.shape=shape
        '''mass=0对应不参与碰撞计算的goal类'''
        self.mass = mass
        """转动惯量"""
        self.j=j
        """恢复系数"""
        self.k=k
        """环境阻力系数"""
        self.f=f
        """n条边"""
        self.n=n
        self.num=num
        self.relative_points=relative_points
        self.radius=radius
        self.color = color
        self.c=c


        self.father = father
        self.son = []
        self.last = last
        self.next=[]
        self.set_tree()

        self.fixed = fixed
        self.draw = draw
        self.collision_detection = collision_detection
        self.collision_calculation = collision_calculation

        self.x=x
        self.x_last=x
        self.y=y
        self.y_last=y

        """(-pi,pi]"""
        self.theta = theta
        self.relative_theta=0
        self.delta_theta=0
        self.theta0=0
        self.theta_last=theta
        self.realtime_theta=self.get_realtime_theta()
        self.w=0.0


        self.x_dot=x_dot
        self.y_dot=y_dot
        self.v =get_norm_of_vector((self.x_dot, self.y_dot))
        self.theta_v = get_theta_of_vector((self.x_dot, self.y_dot))

        #self.resistance_v_dot=-20
        #self.resistance_w_dot=0.5


        self.realtime_points=self.get_realtime_points()
        self.position_colliding=None
        self.colliding_list=[]
        self.set_list()

        self.pic_address=pic_address


    def set_tree(self):
        if self.last==None :
            self.last=self
        else:
            self.last.next.append(self)
        if self.father==None:
            self.father =self
        else:
            self.father.son.append(self)

    def set_list(self):
        all_obj.append(self)
        if self.father==self:
            father_obj.append(self)
        if self.draw==True :
            obj_draw.append(self)
        if self.shape=='polygon':
            obj_polygon.append(self )
        if self.shape=='circle':
            obj_circle.append(self )
        if self.collision_detection==True :
            collision_detection.append(self )
        """
        if self.collision_calculation==True :
            collision_calculation.append(self )
        """




    def set_relative_edges(self):
        relative_edges={}
        for i in range(self.n):
            relative_edges["e%d" % i]=vector_minus(self.relative_points["p%d" % ((i + 1) % self.n)], self.relative_points["p%d" % (i % self.n)])
        return relative_edges
    def set_relative_normal_edges(self):
        "设置每条边的单位法向量"
        relative_normal_edges={}
        for i in range(self.n):
            temp_1=get_normal_vector(self.relative_edges["e%d" % i])
            temp_2=self.relative_points["p%d" % i]
            if vector_point_mutiple(temp_1,temp_2)<0:
                temp_1=(-temp_1[0],-temp_1[1])
            temp_1=get_direction_vector(temp_1)
            relative_normal_edges["e%d" % i]=temp_1
        return relative_normal_edges



    def set_range_of_relative_vector_projection_norm(self):
        """返回一个字典，对于每个边，字典的值为其所有相对点坐标在该边法向上投影/单位法向量比值的（最小值，最大值）,格式：dict_of_range={e1:(最小，最大)}"""
        dict_of_range={}
        range_of_relative_vector_projection_x={}
        for i in range(self.n):
            relative_normal_edge=self.relative_normal_edges["e%d" % i]
            for j in range(self.n):
                vector=get_vector_from_vector_projection(self.relative_points["p%d" % j],relative_normal_edge )
                if relative_normal_edge[0]!=0:
                    k=vector[0]/relative_normal_edge[0]
                else:
                    k=vector[1]/relative_normal_edge[1]
                if j==0:
                    range_of_relative_vector_projection_x["r0" ]=k
                elif j==1:
                    if k<range_of_relative_vector_projection_x["r0"] :
                        range_of_relative_vector_projection_x["r1"]=range_of_relative_vector_projection_x["r0"]
                        range_of_relative_vector_projection_x["r0"]=k
                    elif k>=range_of_relative_vector_projection_x["r0"] :
                        range_of_relative_vector_projection_x["r1"]=k
                elif j>=2:
                    if k<range_of_relative_vector_projection_x["r0"] :
                        range_of_relative_vector_projection_x["r0"]=k
                    elif k>=range_of_relative_vector_projection_x["r1"]:
                        range_of_relative_vector_projection_x["r1"]=k
            dict_of_range["e%d" % i]=(range_of_relative_vector_projection_x["r0"],range_of_relative_vector_projection_x["r1"])

        return dict_of_range





    def get_realtime_points(self):
        realtime_points={}
        for i in range(self.n):
            temp = vector_rotate(self.relative_points["p%d" % i], self.get_realtime_theta())
            realtime_points["p%d" % i] = vector_plus(temp, (self.x, self.y))
        return realtime_points
    """
        def get_realtime_joint_points(self):
        realtime_joint_points={}
        for i in range(len(self.joint_points)):
            temp=vector_rotate(self.joint_points["p%d" % i],self.realtime_theta)
            realtime_joint_points["p%d" % i] = vector_plus(temp, (self.x, self.y))
        return realtime_joint_points
    """


    def get_realtime_theta(self):
        if self.last==self :
            realtime_theta=self.theta
            return realtime_theta
        else:
            realtime_theta=self.theta+self.last.realtime_theta+self.relative_theta+self.delta_theta
            '''if self.name=="fish_tail":
                print("tail_relative_theta=",self.relative_theta )'''
            return realtime_theta

    def get_realtime_edges(self):
        realtime_edges={}
        for i in range(self.n):
            realtime_edges["e%d" % i]=vector_rotate(self.relative_edges["e%d" % i],self.theta)
        return realtime_edges

    def get_realtime_normal_edges(self):
        pass
        """
        realtime_normal_edges={}
        for i in range(self.n):
            realtime_normal_edges["e%d" % i] = vector_rotate(self.relative_normal_edges["e%d" % i],self.theta)
        return realtime_normal_edges
        """

    def set_v_and_theta_v(self):
        self.v = math.sqrt(self.x_dot * self.x_dot + self.y_dot * self.y_dot)
        self.theta_v = get_theta_of_vector((self.x_dot, self.y_dot))

    def set_x_dot_and_y_dot(self):
        self.x_dot = self.v * math.cos(self.theta_v)
        self.y_dot = self.v * math.sin(self.theta_v)

    def update(self):
        pass



'''
class Fish(physics ):
    def __init__(self, name, shape, mass, n, relative_points, color, x,y,x_dot, y_dot, radius):
        super(Fish ,self ).__init__(name=name, shape=shape, mass=mass, n=n, relative_points=relative_points, color=color,x=x,y=y, x_dot=x_dot, y_dot=y_dot)
        self.radius = radius
        self.core = self.get_core()
'''

class Circle(physics ):
    def __init__(self, name, num,shape, mass, n, relative_points, color, x,y,x_dot, y_dot, radius,last=None,father=None):
        physics.__init__(self,name=name, num=num,shape=shape, mass=mass, n=n, relative_points=relative_points, color=color,x=x,y=y, x_dot=x_dot, y_dot=y_dot,last=last,father=father)
        """circle代表包络圆，core为包络圆的圆心，用于碰撞初步检测，圆形物体无需此项"""
        self.have_circle=False
        self.radius = radius
        self.core = (x,y)
        self.j=200000

    def get_core(self):
        """寻找外包圆形对应的圆心"""
        total = (0, 0)
        for i in range(self.n):
            total = vector_plus(total, self.realtime_points["p%d" % i])
        return (total[0] / self.n, total[1] / self.n)
class goal(Circle):
    "判定碰撞，但不参与碰后计算"
    def __init__(self, name, num,shape, n, relative_points, color, x,y,x_dot, y_dot, radius=0,mass=0,draw_radius=30):
        Circle.__init__(self, name=name, num=num,shape=shape, mass=mass, n=n, relative_points=relative_points, color=color,x=x,y=y, x_dot=x_dot, y_dot=y_dot, radius=radius)
        self.draw_radius=draw_radius
        self.fixed=True
        self.collision_calculation=False



class Polygon(physics):
    def __init__(self, name="unnamed", num=0,shape="polygon", mass=99999, j=18000,n=0, relative_points={},joint_points={},joint_num=None, color=(0,0,0),x=0, y=0, x_dot=0.0, y_dot=0.0, theta=0.0, fixed=False, draw=True, collision_detection=True, have_circle=True,collision_calculation=True, last=None,father=None,pic_address=None):
        physics.__init__(self,name=name, num=num,shape=shape, mass=mass, j=j,n=n, relative_points=relative_points,joint_points=joint_points,joint_num=joint_num,color=color, x=x, y=y, x_dot=x_dot, y_dot=y_dot, theta=theta, fixed=fixed, last=last,father=father,draw=draw, collision_detection=collision_detection, collision_calculation=collision_calculation,pic_address=pic_address)

        self.have_circle=have_circle
        self.relative_edges=self.set_relative_edges()
        self.relative_normal_edges=self.set_relative_normal_edges()
        self.range_of_relative_vector_projection_norm=self.set_range_of_relative_vector_projection_norm()




        self.realtime_edges=self.get_realtime_edges()
        self.realtime_normal_edges=self.get_realtime_normal_edges()
        #self.j=j
        if self.have_circle==True:
            self.core = self.get_core()
            self.radius = self.get_radius()

    def set_relative_edges(self):
        relative_edges={}
        for i in range(self.n):
            relative_edges["e%d" % i]=vector_minus(self.relative_points["p%d" % ((i + 1) % self.n)], self.relative_points["p%d" % (i % self.n)])
        return relative_edges
    def set_relative_normal_edges(self):
        "设置每条边的单位法向量"
        relative_normal_edges={}
        for i in range(self.n):
            temp_1=get_normal_vector(self.relative_edges["e%d" % i])
            temp_2=self.relative_points["p%d" % i]
            if vector_point_mutiple(temp_1,temp_2)<0:
                temp_1=(-temp_1[0],-temp_1[1])
            temp_1=get_direction_vector(temp_1)
            relative_normal_edges["e%d" % i]=temp_1
        return relative_normal_edges
    def get_radius(self):
        r=0
        for i in range(self.n):
            r_temp=get_norm_of_vector(vector_minus(self.realtime_points["p%d" % i],self.core) )
            if r_temp>r:
                r=r_temp
        return r
    def get_core(self):
        """寻找外包圆形对应的圆心"""
        total=(0,0)
        for i in range(self.n):
            total=vector_plus(total, self.realtime_points["p%d" % i])
        return (total[0]/self.n,total[1]/self.n)



    def set_range_of_relative_vector_projection_norm(self):
        """返回一个字典，对于每个边，字典的值为其所有相对点坐标在该边法向上投影/单位法向量比值的（最小值，最大值）,格式：dict_of_range={e1:(最小，最大)}"""
        dict_of_range={}
        range_of_relative_vector_projection_x={}
        for i in range(self.n):
            relative_normal_edge=self.relative_normal_edges["e%d" % i]
            for j in range(self.n):
                vector=get_vector_from_vector_projection(self.relative_points["p%d" % j],relative_normal_edge )
                if relative_normal_edge[0]!=0:
                    k=vector[0]/relative_normal_edge[0]
                else:
                    k=vector[1]/relative_normal_edge[1]
                if j==0:
                    range_of_relative_vector_projection_x["r0" ]=k
                elif j==1:
                    if k<range_of_relative_vector_projection_x["r0"] :
                        range_of_relative_vector_projection_x["r1"]=range_of_relative_vector_projection_x["r0"]
                        range_of_relative_vector_projection_x["r0"]=k
                    elif k>=range_of_relative_vector_projection_x["r0"] :
                        range_of_relative_vector_projection_x["r1"]=k
                elif j>=2:
                    if k<range_of_relative_vector_projection_x["r0"] :
                        range_of_relative_vector_projection_x["r0"]=k
                    elif k>=range_of_relative_vector_projection_x["r1"]:
                        range_of_relative_vector_projection_x["r1"]=k
            dict_of_range["e%d" % i]=(range_of_relative_vector_projection_x["r0"],range_of_relative_vector_projection_x["r1"])

        return dict_of_range


    def get_realtime_points(self):
        realtime_points={}
        for i in range(self.n):
            temp = vector_rotate(self.relative_points["p%d" % i], self.realtime_theta)
            realtime_points["p%d" % i] = vector_plus(temp, (self.x, self.y))

        return realtime_points

    def get_realtime_edges(self):
        realtime_edges={}
        for i in range(self.n):
            realtime_edges["e%d" % i]=vector_rotate(self.relative_edges["e%d" % i], self.last.theta)
            if self.last!=self:
                realtime_edges["e%d" % i] = vector_rotate(self.relative_edges["e%d" % i], self.last.theta + self.theta)
        return realtime_edges

    def get_realtime_normal_edges(self):
        realtime_normal_edges={}
        for i in range(self.n):
            realtime_normal_edges["e%d" % i] = vector_rotate(self.relative_normal_edges["e%d" % i],self.theta)
            if self.last!=self:
                realtime_normal_edges["e%d" % i] = vector_rotate(self.relative_normal_edges["e%d" % i], self.last.theta + self.theta)
        return realtime_normal_edges
    def set_theta_direction_of_edge(self):
        pass
class Pool(Polygon):
    def __init__(self, name,num, shape, n, relative_points,x,y):
        Polygon.__init__(self,name=name, num=num,mass=99999,shape=shape, n=n, x=x,y=y,relative_points=relative_points,have_circle=False)
        self.fixed=True
        #self.have_been_collided = False


class RobotFish(Polygon):
    def __init__(self,num,name,shape,mass,n,relative_points,color,x,y,x_dot,y_dot,theta):

        self.realtime_theta=theta
        self.theta=theta

        self.last=self
        self.next=[]
        self.son=[]
        self.set_robotfish(num, x, y)


        """影响鱼转动加速度,由w_mode控制"""
        self.w_dot_list = w_dot_list
        self.w_dot_direction = 1
        self.w_dot_number = 0
        self.w_mode = 0
        self.w_dot = self.w_dot_list[self.w_mode]
        """"鱼尾相对摆动角,由w_mode控制"""
        self.relative_theta_list = relative_theta_list
        """鱼尾摆动速度，由v_mode控制"""
        self.tail_waving_list =tail_waving_list
        # self.w_list = []
        self.tail_waving_direction = 1
        # self.w_number=0
        """鱼游动加速度，由v_mode控制"""
        self.v_dot_list=v_dot_list
        self.v_mode=0
        self.v_dot=self.v_dot_list[self.v_mode]
        """鱼的滞后摆动角，由w_mode控制"""
        self.delta_theta_list=delta_theta_list


        self.realtime_theta = self.get_realtime_theta()
        self._next=self.next
        self._son=self.son
        self.relative_points = self.get_relative_points()
        Polygon.__init__(self,name=name,num=num,shape=shape,mass=mass,n=n,relative_points=self.relative_points,color=color,x=x,y=y,x_dot=x_dot,y_dot=y_dot,theta=theta,draw=False  ,collision_detection=True  )
        #self.set_theta_direction_of_edge()
        self.next=self._next
        self.son=self._son

        self.have_circle=True
        if self.have_circle==True:
            self.radius=self.get_radius()
            self.core=self.get_core()
        self.j = 30000



    def set_robotfish(self,num,x,y):
        self.fish_head = Circle("fish_head",num,'circle', mass=10, n=1,relative_points={'p0':(20,0)},radius=10,x=0,y=0,x_dot=0,y_dot=0,color=(20, 120, 200),last=self,father=self)

        '''self.fish_head = Polygon("fish_head", 'polygon', mass=10, n=4,
                                 relative_points={'p0': (40, -3),'p1':(40,3), 'p2': (20, 10), 'p3': (20, -10)}, color=(20, 120, 200),
                                 theta=0, collision_detection=True, collision_calculation=False,
                                 last=self, father=self)'''
        '''self.fish_head=Polygon ("fish_head",'polygon',mass=8,  n=3, relative_points= {'p0':(40,0),'p1':(20,10),'p2':(20,-10)}, color=(20, 120, 200),theta=0, collision_detection=True ,collision_calculation=False,
                                last=self ,father=self)'''
        self.fish_body1=Polygon("fish_body1",num, 'polygon', mass=10, n=4, relative_points={'p0':(20,10), 'p1':(-10,10), 'p2':(-10,-10), 'p3':(20,-10)}, color=(20, 120, 200),x=x, y=y, theta=0, collision_detection=True,
                                last=self,father=self)
        self.fish_body2=Polygon("fish_body2",num,'polygon', mass=0.4, n=4, relative_points={'p0':(0,10),'p1':(-20,5),'p2':(-20,-5),'p3':(0,-10)}, color=(20, 120, 200), x=-10+x, y=y, theta=0, collision_detection=True  ,
                                last=self,father=self)
        self.fish_body3 = Polygon("fish_body3", num, 'polygon', mass=0.4, n=3,
                                  relative_points={'p0': (0, 5), 'p1': (-20, 0), 'p2': (0, -5)}, color=(20, 120, 200),
                                  x=-40 + x, y=y, theta=0, collision_detection=True,
                                  last=self.fish_body2, father=self)
        self.fish_tail=Polygon("fish_tail",num,'polygon',mass=0.4,  n=3, relative_points={'p0':(0,0),'p1':(-20,2),'p2':(-20,-2)}, color=(20, 120, 200), theta=0, collision_detection=True ,
                               last=self.fish_body3,father=self)
        self.robotfish_list=[self.fish_head,self.fish_body1,self.fish_body2 ,self.fish_body3,self.fish_tail ]

    def get_core(self):
        return vector_multiple(vector_plus(self.realtime_points['p2'],self.realtime_points['p4']),0.5)
    def get_radius(self):
        r=61
        return r

    def get_relative_points(self):
        _dict={'p0':self.fish_head.relative_points['p0'],'p1':self.fish_body1.relative_points['p0'],'p2':self.fish_body1.relative_points['p1'],'p3':self.fish_body2.relative_points['p1'],'p4':self.fish_body1.relative_points['p2'],'p5':self.fish_body1.relative_points['p3']}
        return _dict
    def get_realtime_points(self):
        _dict={'p0':self.fish_head.realtime_points['p0'],'p1':self.fish_body1.realtime_points['p0'],'p2':self.fish_body1.realtime_points['p1'],'p3':vector_multiple(vector_plus(self.fish_tail.realtime_points['p1'],self.fish_tail.realtime_points['p2']),0.5) ,'p4':self.fish_body1.realtime_points['p2'],'p5':self.fish_body1.realtime_points['p3']}
        return _dict
    def fish_body2_update(self):
        a = self.fish_body2
        (a.x, a.y) = vector_multiple(
            vector_plus(self.fish_body1.realtime_points['p1'], self.fish_body1.realtime_points['p2']), 0.5)
        a.realtime_theta = a.theta + a.last.realtime_theta
    def fish_tail_update(self):
        a = self.fish_tail
        (a.x, a.y) = self.fish_body2.realtime_points['p1']
        a.realtime_theta = a.theta + a.last.realtime_theta
    def update(self):
        for a in self.robotfish_list:
            (a.x,a.y)=(self.x,self.y)
            if a == self.fish_body2:
                (a.x, a.y) = vector_multiple(
                    vector_plus(self.fish_body1.realtime_points['p1'], self.fish_body1.realtime_points['p2']), 0.5)
                a.relative_theta = self.relative_theta_list[self.w_mode] * self.w_dot_direction*-1
            if a==self.fish_body3:
                (a.x,a.y)=vector_multiple(
                    vector_plus(self.fish_body2.realtime_points['p1'], self.fish_body2.realtime_points['p2']), 0.5)
                a.relative_theta = self.relative_theta_list[self.w_mode] * self.w_dot_direction*-1
            if a==self.fish_tail:
                (a.x,a.y)=self.fish_body3.realtime_points['p1']
                a.relative_theta = self.relative_theta_list[self.w_mode] * self.w_dot_direction*-1

            a.realtime_theta=a.get_realtime_theta()
            a.realtime_points=a.get_realtime_points()
            a.core = a.get_core()
    '''def apply_mode(self):
        self.v_dot_number=self.v_mode
        self.w_dot_number=self.w_mode
        self.fish_body2.w_number=self.v_mode
        self.fish_body2.relative_theta_number=self.w_mode
'''
    def wave_tail(self):
        max_theta=0.5
        for a in self.robotfish_list:
            if a==self.fish_body2:
                '''a.w_number=self.v_dot_number'''
                if a.theta>max_theta:
                    self.tail_waving_direction=-1
                if a.theta<-max_theta:
                    self.tail_waving_direction=1
                a.w=self.tail_waving_list[self.v_mode]*self.tail_waving_direction
                a.theta= a.theta + a.w*timestep
                """a.relative_theta=a.relative_theta_list[self.w_mode]*self."""
            elif a==self.fish_body3:
                '''a.w_number=self.v_dot_number'''
                a.delta_theta=-self.delta_theta_list[self.w_mode] * self.w_dot_direction
                if a.theta+a.delta_theta>max_theta:
                    self.tail_waving_direction=-1
                if a.theta+a.delta_theta<-max_theta:
                    self.tail_waving_direction=1
                a.w=self.tail_waving_list[self.v_mode]*self.tail_waving_direction

            elif a==self.fish_tail:
                a.delta_theta = -self.delta_theta_list[self.w_mode] * self.w_dot_direction
                if a.theta+a.delta_theta > max_theta:
                    self.tail_waving_direction= -1
                if a.theta+a.delta_theta < -max_theta:
                    self.tail_waving_direction= 1
                a.w=self.tail_waving_list[self.v_mode]*self.tail_waving_direction

