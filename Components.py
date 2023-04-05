class Square:
    def __init__(self, x_pos, y_pos, width, height, pg, colour=(180, 241, 255), hover_colour=None,
                 text=None, text_colour=None, text_font=None):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.width = width
        self.height = height
        self.colour = colour
        self.hover_colour = hover_colour
        self.text_colour = text_colour
        self.rect = pg.Rect(x_pos, y_pos, width, height)
        self.text_font = text_font
        self.text = None
        self.text_rect = None
        if text is not None:
            self.text = text_font.render(text, True, text_colour)
            self.text_rect = self.text.get_rect(
                center=(x_pos + (width // 2), y_pos + (height // 2))
            )

