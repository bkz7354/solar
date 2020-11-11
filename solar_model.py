import copy


class Model:
    def __init__(self, objects, time=0):
        self.objects = copy.deepcopy(objects)
        self.time = time

    def update(self, time_delta):
        self.time += time_delta

        # TODO everything else

    def get_objects(self):
        return copy.deepcopy(self.objects)