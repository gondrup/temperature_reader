from tempocr import segments

class ImageCoordinates:
    def __init__(self, x_ratio, y_ratio):
        self.x_ratio = x_ratio
        self.y_ratio = y_ratio

    def get_pixel_x(self, image):
        width, height = image.size
        return int(round(self.x_ratio * width, 0))

    def get_pixel_y(self, image):
        width, height = image.size
        return int(round(self.y_ratio * height, 0))

    def get_pixel(self, image):
        width, height = image.size
        return (self.get_pixel_x(image), self.get_pixel_y(image))

bg_color_coords = [
    ImageCoordinates(0.075, 0.14375),
    ImageCoordinates(0.1390625, 0.1416666667),
    ImageCoordinates(0.6765625, 0.2),
    ImageCoordinates(0.3109375, 0.375),
    ImageCoordinates(0.51875, 0.3770833333),
    ImageCoordinates(0.7328125, 0.3895833333),
    ImageCoordinates(0.9296875, 0.1416666667),
    ImageCoordinates(0.9453125, 0.4041666667),
    ImageCoordinates(0.2578125, 0.5833333333),
    ImageCoordinates(0.040625, 0.9458333333),
    ImageCoordinates(0.4796875, 0.8604166667),
    ImageCoordinates(0.6984375, 0.69375),
    ImageCoordinates(0.9234375, 0.6479166667)
]

fg_color_coords = [
    ImageCoordinates(0.9078125, 0.8416666667),
    ImageCoordinates(0.940625, 0.2833333333),
    ImageCoordinates(0.903125, 0.3333333333),
    ImageCoordinates(0.8953125, 0.4375),
    ImageCoordinates(0.928125, 0.4833333333),
    ImageCoordinates(0.6265625, 0.4958333333)
]

def get_bg_colors(image):
    colors = []

    for coords in bg_color_coords:
        colors.append(image.getpixel(coords.get_pixel(image)))

    return colors

def get_fg_colors(image):
    colors = []

    for coords in fg_color_coords:
        colors.append(image.getpixel(coords.get_pixel(image)))

    return colors

def get_digits(image):
    # Define the known digits/segments

    rgb_image = image.convert('RGB')

    # Get the BG and FG colours from known points on the image
    bg_colors = get_bg_colors(rgb_image)
    fg_colors = get_fg_colors(rgb_image)

    return [
        # TODO: Add MinusSeg and TwoSeg (need to find on screen)
        #segments.MinusSeg([
        #    segments.SegmentStripe(rgb_image, (240, 322), (220, 412)) # Check this, guessed numbers
        #], bg_colors, fg_colors),
        #segments.TwoSeg([
        #    segments.SegmentStripe(rgb_image, (93, 176), (114, 177)), # Check this, guessed numbers
        #    segments.SegmentStripe(rgb_image, (99, 84), (118, 86)) # Check this, guessed numbers
        #], bg_colors, fg_colors),
        segments.SevenSeg([
            segments.SegmentStripe(rgb_image, ImageCoordinates(0.3203125, 0.05416666667).get_pixel(image), ImageCoordinates(0.31875, 0.125).get_pixel(image)),
            segments.SegmentStripe(rgb_image, ImageCoordinates(0.359375, 0.18125).get_pixel(image), ImageCoordinates(0.4078125, 0.18125).get_pixel(image)),
            segments.SegmentStripe(rgb_image, ImageCoordinates(0.340625, 0.375).get_pixel(image), ImageCoordinates(0.3890625, 0.375).get_pixel(image)),
            segments.SegmentStripe(rgb_image, ImageCoordinates(0.3, 0.43125).get_pixel(image), ImageCoordinates(0.296875, 0.5).get_pixel(image)),
            segments.SegmentStripe(rgb_image, ImageCoordinates(0.2078125, 0.36875).get_pixel(image), ImageCoordinates(0.2578125, 0.36875).get_pixel(image)),
            segments.SegmentStripe(rgb_image, ImageCoordinates(0.215625, 0.175).get_pixel(image), ImageCoordinates(0.2640625, 0.1770833333).get_pixel(image)),
            segments.SegmentStripe(rgb_image, ImageCoordinates(0.3078125, 0.24375).get_pixel(image), ImageCoordinates(0.30625, 0.3125).get_pixel(image))
        ], bg_colors, fg_colors),
        segments.SevenSeg([
            segments.SegmentStripe(rgb_image, ImageCoordinates(0.5375, 0.05416666667).get_pixel(image), ImageCoordinates(0.5359375, 0.1229166667).get_pixel(image)),
            segments.SegmentStripe(rgb_image, ImageCoordinates(0.575, 0.18125).get_pixel(image), ImageCoordinates(0.625, 0.18125).get_pixel(image)),
            segments.SegmentStripe(rgb_image, ImageCoordinates(0.55625, 0.375).get_pixel(image), ImageCoordinates(0.60625, 0.3729166667).get_pixel(image)),
            segments.SegmentStripe(rgb_image, ImageCoordinates(0.5171875, 0.43125).get_pixel(image), ImageCoordinates(0.5140625, 0.5).get_pixel(image)),
            segments.SegmentStripe(rgb_image, ImageCoordinates(0.425, 0.36875).get_pixel(image), ImageCoordinates(0.475, 0.36875).get_pixel(image)),
            segments.SegmentStripe(rgb_image, ImageCoordinates(0.4328125, 0.1770833333).get_pixel(image), ImageCoordinates(0.4828125, 0.175).get_pixel(image)),
            segments.SegmentStripe(rgb_image, ImageCoordinates(0.5265625, 0.24375).get_pixel(image), ImageCoordinates(0.521875, 0.3125).get_pixel(image))
        ], bg_colors, fg_colors),
        segments.PointSeg([
            segments.SegmentStripe(rgb_image, ImageCoordinates(0.615625, 0.4854166667).get_pixel(image), ImageCoordinates(0.6375, 0.4854166667).get_pixel(image))
        ], bg_colors, fg_colors),
segments.SevenSeg([
        segments.SegmentStripe(rgb_image, ImageCoordinates(0.765625, 0.05416666667).get_pixel(image), ImageCoordinates(0.7640625, 0.1229166667).get_pixel(image)),
            segments.SegmentStripe(rgb_image, ImageCoordinates(0.803125, 0.1791666667).get_pixel(image), ImageCoordinates(0.8515625, 0.18125).get_pixel(image)),
            segments.SegmentStripe(rgb_image, ImageCoordinates(0.790625, 0.3729166667).get_pixel(image), ImageCoordinates(0.8390625, 0.375).get_pixel(image)),
            segments.SegmentStripe(rgb_image, ImageCoordinates(0.74375, 0.43125).get_pixel(image), ImageCoordinates(0.740625, 0.5020833333).get_pixel(image)),
            segments.SegmentStripe(rgb_image, ImageCoordinates(0.653125, 0.36875).get_pixel(image), ImageCoordinates(0.703125, 0.36875).get_pixel(image)),
            segments.SegmentStripe(rgb_image, ImageCoordinates(0.659375, 0.1770833333).get_pixel(image), ImageCoordinates(0.709375, 0.1770833333).get_pixel(image)),
            segments.SegmentStripe(rgb_image, ImageCoordinates(0.753125, 0.24375).get_pixel(image), ImageCoordinates(0.75, 0.3145833333).get_pixel(image))
        ], bg_colors, fg_colors)
    ]

def read_temperature(image):
    digits = get_digits(image)

    '''
    # Draw lines on image to stdout
    for digit in digits:
        digit.draw_on_image()

    rgb_image.save(sys.stdout, "PNG")
    '''

    temperature = ''
    for digit in digits:
        temperature += digit.get_digit()

    return temperature