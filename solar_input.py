from solar_obj import Object
import colors

# write down data in table
def save_to_file(objects, filename):
    input = open(filename, 'w')
    input.write("Object's coords".center(20) + "Radius".center(10) +
                "Color".center(10) + "Mass".center(10) + "Velocity".center(20) + '\n')
    for item in objects:
        input.write(str(item.coord).center(20) + str(item.rad).center(10) +
                    str(item.col).center(10) + str(item.mass).center(10) + str(item.vel).center(20) + '\n')
    input.close()
    print("dummy save to " + filename)


def parse_object(line):
    # data order: type radius color mass x y vx vy
    data = line.split()

    radius = int(data[1])
    col = colors.color_dict[data[2]]
    mass = float(data[3])
    coords = [float(x) for x in data[4:6]]
    vel = [float(x) for x in data[6:8]]
    
    
    return Object(coords, radius, col, mass, vel)
    


# read off data from table
def load_from_file(filename):
    objects = []
    with open(filename) as file:
        lines = file.readlines()
        for line in lines:
            line = line.strip()
            if line and line[0] != '#':
                try:
                    objects.append(parse_object(line))
                except:
                    print("Skipping line: " + line)
        

    print("Loaded " + str(len(objects)) + " objects from " + filename)
    print(objects[0].coord)
    print(objects[1].coord)
    return objects
