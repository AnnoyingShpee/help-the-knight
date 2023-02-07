class Square:
    def __init__(self, x_pos, y_pos, width, height, pg, color=(180, 241, 255), text_colour=None, hover_colour=None):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.width = width
        self.height = height
        self.color = color
        self.text_color = text_colour
        self.hover_color = hover_colour
        self.rect = pg.Rect(x_pos, y_pos, width, height)
