BACKGROUND_COLOUR = (180, 241, 255)


class Button:
    def __init__(self, x_pos, y_pos, width, height, color, hover_colour=None, text_colour=None):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.width = width
        self.height = height
        self.color = color
        self.hover_color = hover_colour
        self.text_color = text_colour


class TextArea:
    def __init__(self, x_pos, y_pos, width, height, text_colour, background_colour=BACKGROUND_COLOUR):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.width = width
        self.height = height
        self.text_color = text_colour
        self.background_colour = background_colour
