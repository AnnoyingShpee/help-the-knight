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
        self.text = text
        self.text_font = None
        self.text_render = None
        self.text_rect = None
        if text is not None:
            self.text_font = text_font
            self.text_render = text_font.render(text, True, text_colour)
            self.text_rect = self.text_render.get_rect(
                center=(x_pos + (width // 2), y_pos + (height // 2))
            )

    def change_text(self, text):
        self.text = text
        self.text_render = self.text_font.render(self.text, True, self.text_colour)
        self.text_rect = self.text_render.get_rect(
            center=(self.x_pos + (self.width // 2), self.y_pos + (self.height // 2))
        )
