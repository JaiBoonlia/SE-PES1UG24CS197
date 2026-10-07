"""
Brick: a single block. Three kinds:

- NORMAL:      destroyed after 1 hit.
- STRONG:      destroyed after 3 hits; its colour lightens as it is damaged.
- UNBREAKABLE: never destroyed, no matter how often it is hit.
"""

import pygame

NORMAL = "normal"
STRONG = "strong"
UNBREAKABLE = "unbreakable"

# Hits needed to destroy each kind (None = can never be destroyed).
HITS_TO_BREAK = {NORMAL: 1, STRONG: 3, UNBREAKABLE: None}

COLOR_NORMAL = (200, 90, 90)                  # red
COLOR_UNBREAKABLE = (120, 120, 130)           # steel grey
COLOR_STRONG_BY_HITS = {                      # blue, lighter as it weakens
    3: (50, 80, 200),
    2: (100, 135, 235),
    1: (170, 190, 250),
}


class Brick:
    def __init__(self, x, y, width, height, kind=NORMAL):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.kind = kind
        self.hits_remaining = HITS_TO_BREAK[kind]

    @property
    def breakable(self):
        return self.kind != UNBREAKABLE

    @property
    def color(self):
        if self.kind == STRONG:
            return COLOR_STRONG_BY_HITS[max(1, self.hits_remaining)]
        if self.kind == UNBREAKABLE:
            return COLOR_UNBREAKABLE
        return COLOR_NORMAL

    def hit(self):
        """Register one hit. Returns True if the brick is now destroyed."""
        if not self.breakable:
            return False
        self.hits_remaining -= 1
        return self.hits_remaining <= 0

    def get_rect(self):
        return pygame.Rect(int(self.x), int(self.y), self.width, self.height)
