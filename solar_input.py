from solar_obj import Object


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


# read off data from table
def load_from_file(filename):
    objects = []
    output = open(filename, 'r')
    lines = output.readlines()
    del lines[0]  # names of columns are ignored
    for i in range(len(lines)):
        lines[i] = lines[i].replace('[', ',').replace(']', ',').replace(',', '')
    for line in lines:
        tmp = line.split()
        objects.append(Object([float(tmp[0]), float(tmp[1])], float(tmp[2]),
                              (tmp[3]), float(tmp[4]), [float(tmp[5]), float(tmp[6])]))
    output.close()
    print("dummmy load from " + filename)
    return objects
