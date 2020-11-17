from solar_obj import Object
import colors

# write down data in table
def save_to_file(objects, filename):
    try:
        with open(filename, 'w') as file:
            for item in objects:
                print("Planet", item.rad, item.col, item.mass, 
                      item.coord[0], item.coord[1],
                      item.vel[0], item.vel[1], file=file)
            
        print("Saved data to " + filename)
    except:
        print("Error when saving to file")

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
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()
            for line in lines:
                line = line.strip()
                if line and line[0] != '#':
                    try:
                        objects.append(parse_object(line))
                    except:
                        print("Skipping line: " + line)
        print("Loaded " + str(len(objects)) + " objects from " + filename)
    except:
        print("Error when opening file")    

    return objects
