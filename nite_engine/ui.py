from pygame.colordict import THECOLORS as COLORS
from pygame import draw, event, mouse, Surface
from pygame.locals import *
from pygame.font import Font, get_default_font, SysFont


class UIManager:
    default_font = Font(get_default_font(), 18)
    DEBUGMODE = True

    def __init__(self):
        self.elements = []

    def create_element(self, kind):
        new_element = None

        if kind == "none":
            new_element = UIElement()
            self.elements.append(new_element)
        elif kind == "label":
            new_element = UILabel()
            self.elements.append(new_element)
        elif kind == "entry":
            new_element = UIEntry()
            self.elements.append(new_element)
        return new_element

    def on_update(self, dt):
        for element in self.elements:
            element.on_update(dt)

    def on_event(self, events):
        for element in self.elements:
            element.on_event(events)

    def on_draw(self, dest):
        for element in self.elements:
            element.on_draw(dest)


class UIElement:
    def __init__(self):
        self.id = id
        self.name = ""
        self._rect = Rect(0, 0, 100, 20)
        self.parent = None
        self.children = None

        self.hovered = False
        self.r_clicked = False
        self.l_clicked = False
        self.enabled = True
        self.focused = False

        self.background_color = (0, 0, 0, 0)
        self.idle_color = COLORS["white"]
        self.border_color = COLORS["orange"]
        self.hovered_color = COLORS["yellow"]
        self.clicked_color = COLORS["red"]

        self.surface = Surface(self.rect.size, SRCALPHA)
        self.surface.fill(self.background_color)

    @property
    def rect(self, values):
        self._rect = Rect(values)
        self.surface = Surface(self._rect.size, SRCALPHA)

    @rect.getter
    def rect(self):
        return self._rect

    @rect.setter
    def rect(self, values):
        self._rect = Rect(values)
        self.surface = Surface(self._rect.size, SRCALPHA)

    def on_update(self, dt):
        pass

    def on_hover(self):
        pass

    def on_hover_end(self):
        pass

    def on_click(self):
        pass

    def on_release(self, button=0):
        pass

    def on_event(self, events):
        if self.enabled:
            mouse_pos = mouse.get_pos()
            if self.rect.collidepoint(mouse_pos):
                self.hovered = True
                self.on_hover()
            else:
                self. hovered = False

            for event in events:
                if event.type == MOUSEBUTTONDOWN:
                    if self.hovered:
                        if event.button == BUTTON_LEFT:
                            self.on_click()
                            self.l_clicked = True

                        elif event.button == BUTTON_RIGHT:
                            self.r_clicked = True

                elif event.type == MOUSEBUTTONUP:
                    self.on_release(event.button)
                    if event.button == BUTTON_LEFT:
                        self.l_clicked = False

                    elif event.button == BUTTON_RIGHT:
                        self.r_clicked = False

    def on_draw(self, dest):
        if self.enabled:
            self.surface.fill((255, 255, 255))
            dest.blit(self.surface, (self.rect.x, self.rect.y))

        if UIManager.DEBUGMODE:
            draw.rect(self.surface, COLORS["orange"], (0, 0, self.rect.w, self.rect.h), 1)


class UILabel(UIElement):
    def __init__(self, text=""):
        super().__init__()
        self._text = text
        self._font_color = COLORS["black"]
        self._font_size = UIManager.default_font.get_height()
        self._font = UIManager.default_font
        self._align = "left"
        self._padding = [2, 2]

        self.background_color = COLORS["transparent"]
        self.text_surface = self._font.render(text, True, self._font_color, self.background_color)
        self.rect = self.text_surface.get_rect(x=self.rect.x, y=self.rect.y)

        self.rect.w = self.rect.w + self._padding[0]*2
        self.rect.h = self.rect.h + self._padding[1]*2
        self.surface = Surface(self.rect.size, SRCALPHA)
        self.surface.fill(self.background_color)

        if self._align == "left":
            self.surface.blit(self.text_surface, (self._padding[0], self.rect.h / 2 - self.text_surface.get_height() / 2 + self._padding[1]))

        elif self._align == "middle":
            self.surface.blit(self.text_surface, (
                self.rect.w / 2 - self.text_surface.get_width() / 2 + self._padding[0],
                self.rect.h / 2 - self.text_surface.get_height() / 2 + self._padding[1]))

        elif self._align == "right":
            self.surface.blit(self.text_surface, (self.rect.w - self.text_surface.get_width(),
                                                  self.rect.h / 2 - self.text_surface.get_height() / 2))

    @property
    def text(self, text):
        self._text = text
        self.text_surface = self._font.render(text, True, COLORS["white"], self.background_color)

    @text.getter
    def text(self):
        return self._text

    @text.setter
    def text(self, text):
        self._text = text
        self.surface.fill(self.background_color)
        self.text_surface = self._font.render(text, True, self._font_color)
        self.rect = self.text_surface.get_rect(x=self.rect.x, y=self.rect.y)

        self.surface = Surface(self.rect.size, SRCALPHA)
        self.surface.fill(self.background_color)

    @property
    def align(self, justify="left"):
        self._align = justify
        self.text = self._text

    @align.getter
    def align(self):
        return self._align

    @align.setter
    def align(self, justify):
        self._align = justify
        self.text = self._text

    @property
    def font(self, value):
        self._font = value
        self.text = self._text

    @font.getter
    def font(self):
        return self._font

    @font.setter
    def font(self, value):
        self._font = value
        self.text = self._text

    @property
    def font_color(self, color):
        self._font_color = color
        self.text = self._text

    @font_color.getter
    def font_color(self):
        return self._font_color

    @font_color.setter
    def font_color(self, color):
        self._font_color = color
        self.text = self._text

    def on_draw(self, dest):
        super().on_draw(dest)
        self.surface.blit(self.text_surface, (0, 0))
        dest.blit(self.surface, self.rect.topleft)


class UIEntry(UIElement):
    def __init__(self):
        super().__init__()
        self.text_label = UILabel("Test")
        self.cursor_label = UILabel()

    def on_click(self):
        super().on_click()
        self.focused = True

    def on_event(self, events):
        super().on_event(events)
        for event in events:
            if event.type == MOUSEBUTTONDOWN:
                if not self.hovered:
                    self.focused = False

    def on_update(self, dt):
        super().on_update(dt)

    def on_draw(self, dest):
        #super().on_draw(dest)
        if self.focused:
            self.surface.fill(COLORS["red"])
        else:
            self.surface.fill(COLORS["blue"])

        self.text_label.on_draw(dest)
        #dest.blit(self.surface, self.rect.topleft)


