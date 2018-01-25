# http://stackoverflow.com/questions/19914509/python-pil-pixel-rgb-color-to-hex
def rgb2hex(pixel):
    return '#{:02x}{:02x}{:02x}'.format(pixel[0], pixel[1], pixel[2])