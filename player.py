import pygame as pgappearance

"""
    A character has a set of properties called their "appearance" which is used when rendering them. 
    Each appearance contains several properties. To begin with it may simply be a single value which
    represents which sprite/graphic will be used when rendering them, but more complex appearances may
    include individual values representing things like which head, hair, body, clothes, and other equipment
    sprites will be used when rendering them.
"""


class Character:
    def __init__(self, name, position, appearance):
        self.name = name
        self.position = position
        self.appearance = appearance