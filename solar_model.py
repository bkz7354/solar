import copy
import math as m


class Model:
    def __init__(self, objects, time=0):
        self.objects = copy.deepcopy(objects)
        self.time = time
        self.calculate_scale()

    def update(self, time_delta):
        self.time += time_delta
        # cycle makes calculations more precise
        time_delta /= 100
        for i in range(100):
            for obj_i in self.objects:
                total_force_x = 0
                total_force_y = 0
                for obj_j in self.objects:
                    if obj_i != obj_j:
                        total_force_x += self.get_force(obj_i, obj_j)*(obj_j.coord[0]-obj_i.coord[0])/self.dist(obj_i, obj_j)
                        total_force_y += self.get_force(obj_i, obj_j)*(obj_j.coord[1]-obj_i.coord[1])/self.dist(obj_i, obj_j)
                obj_i.vel[0] += total_force_x/obj_i.mass*time_delta
                obj_i.vel[1] += total_force_y/obj_i.mass*time_delta
                obj_i.coord[0] += obj_i.vel[0]*time_delta
                obj_i.coord[1] += obj_i.vel[1]*time_delta

    def dist(self, obj1, obj2):
        return m.sqrt((obj1.coord[0]-obj2.coord[0])**2+(obj1.coord[1]-obj2.coord[1])**2)

    def get_force(self, obj1, obj2):
        d = self.dist(obj1, obj2)
        return 1/50*obj1.mass*obj2.mass/d**2

    def calculate_scale(self):
        max_distance = 1
        for obj1 in self.objects:
            max_distance = max(max_distance, m.sqrt(obj1.coord[0]**2 + obj1.coord[1]**2))
            for obj2 in self.objects:
                max_distance = max(max_distance, self.dist(obj1, obj2))
        self.scale_factor = 0.4/max_distance
