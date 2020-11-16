import colors as col


class Object:
    def __init__(self, coord, rad, col, mass, vel):
        self.coord = coord
        self.rad = rad
        self.col = col
        self.mass = mass
        self.vel = vel
