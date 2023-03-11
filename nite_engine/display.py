import pygame as pg
from pygame.colordict import THECOLORS as COLORS


class Display:
    pg.init()

    def __init__(self, size, title, flags=0):
        self.surface = pg.display.set_mode(size, flags, vsync=True)
        self.frame_clock = pg.time.Clock()
        self.frame_rate = 120
        self.dt = 1
        pg.display.set_caption(title)

    @property
    def size(self):
        return self.surface.get_size()

    @size.getter
    def size(self):
        return self.surface.get_size()

    @property
    def width(self):
        return self.surface.get_width()

    @width.getter
    def width(self):
        return self.surface.get_width()

    @property
    def height(self):
        return self.surface.get_height()

    @height.getter
    def height(self):
        return self.surface.get_height()

    @property
    def caption(self):
        return pg.display.get_caption()

    @caption.getter
    def caption(self):
        return pg.display.get_caption()

    @caption.setter
    def caption(self, value):
        pg.display.set_caption(value)

    def clear(self, color=COLORS["black"]):
        self.surface.fill(color)

    def update(self):
        pg.display.update()
        self.dt = self.frame_clock.tick(self.frame_rate)

    def blit(self, source, position):
        self.surface.blit(source, position)
