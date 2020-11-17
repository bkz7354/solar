# utility file with colors for


black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)
orange = (250, 104, 0)
cyan = (0, 255, 255)


color_dict = {
    'white': white,
    'black': black,
    'red': red,
    'green': green,
    'blue': blue,
    'yellow': yellow,
    'orange': orange,
    'cyan': cyan
}

def get_color_name(rgb):
    for key, val in color_dict.items():
        if val == rgb:
            return key
    
    raise Exception("No matching color found")