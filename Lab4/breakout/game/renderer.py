"""
renderer: all pygame drawing lives here, kept separate from game logic.
"""

import pygame

from game.brick import STRONG, UNBREAKABLE

WIDTH, HEIGHT = 640, 520
WINDOW_SIZE = (WIDTH, HEIGHT)

COLOR_BG = (20, 20, 30)
COLOR_PADDLE = (80, 180, 255)
COLOR_BALL = (240, 240, 240)
COLOR_TEXT = (255, 255, 255)


def draw_scene(surface, paddle, ball, bricks):
    surface.fill(COLOR_BG)
    for brick in bricks:
        rect = brick.get_rect()
        pygame.draw.rect(surface, brick.color, rect)
        pygame.draw.rect(surface, (10, 10, 15), rect, 1)
        if brick.kind == STRONG:
            # Bright inner outline marks multi-hit bricks.
            pygame.draw.rect(surface, (230, 235, 255), rect.inflate(-6, -6), 2)
        elif brick.kind == UNBREAKABLE:
            # Dark cross marks bricks that can't be broken.
            pygame.draw.line(surface, (50, 50, 60), rect.topleft, rect.bottomright, 2)
            pygame.draw.line(surface, (50, 50, 60), rect.topright, rect.bottomleft, 2)
    pygame.draw.rect(surface, COLOR_PADDLE, paddle.get_rect(), border_radius=4)
    pygame.draw.circle(surface, COLOR_BALL, (int(ball.x), int(ball.y)), ball.radius)


def draw_text(surface, font, text, pos, color=COLOR_TEXT):
    surface.blit(font.render(text, True, color), pos)


def draw_banner(surface, font, text, dy=0):
    surf = font.render(text, True, (255, 220, 80))
    rect = surf.get_rect(center=(surface.get_width() // 2, surface.get_height() // 2 + dy))
    surface.blit(surf, rect)
