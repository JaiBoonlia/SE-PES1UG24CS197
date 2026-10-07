"""
GameEngine: owns the paddle, ball, and bricks.

Task 2: the player has 3 lives. Missing the ball costs one life and
resets the ball; at 0 lives the game ends and R restarts it.
Task 3: three brick types (normal / strong / unbreakable). The level is
cleared once every breakable brick is gone.
"""

import pygame

from game.paddle import Paddle
from game.ball import Ball
from game.brick import Brick, NORMAL, STRONG, UNBREAKABLE
from game.collision import handle_ball_brick_collision
from game.renderer import WIDTH, HEIGHT

# Level layout: N = normal, S = strong, U = unbreakable.
LAYOUT = [
    "SSSSSSSS",
    "NNNNNNNN",
    "NUNNNNUN",
    "NNNNNNNN",
]
KIND_BY_CHAR = {"N": NORMAL, "S": STRONG, "U": UNBREAKABLE}
BRICK_ROWS = len(LAYOUT)
BRICK_COLS = len(LAYOUT[0])
BRICK_WIDTH = 68
BRICK_HEIGHT = 22
BRICK_GAP = 6
BRICK_TOP_MARGIN = 50
STARTING_LIVES = 3


class GameEngine:
    def __init__(self):
        self.restart()

    def restart(self):
        """Put everything back to a fresh game (also used on first start)."""
        self.paddle = Paddle(x=WIDTH / 2, y=HEIGHT - 30)
        self.ball = Ball(x=WIDTH / 2, y=HEIGHT - 50)
        self.bricks = self._build_bricks()
        self.lives = STARTING_LIVES
        self.game_over = False
        self.won = False

    def _build_bricks(self):
        bricks = []
        total_width = BRICK_COLS * (BRICK_WIDTH + BRICK_GAP) - BRICK_GAP
        start_x = (WIDTH - total_width) / 2
        for row in range(BRICK_ROWS):
            for col in range(BRICK_COLS):
                x = start_x + col * (BRICK_WIDTH + BRICK_GAP)
                y = BRICK_TOP_MARGIN + row * (BRICK_HEIGHT + BRICK_GAP)
                kind = KIND_BY_CHAR[LAYOUT[row][col]]
                bricks.append(Brick(x, y, BRICK_WIDTH, BRICK_HEIGHT, kind))
        return bricks

    def _reset_ball(self):
        self.ball = Ball(x=WIDTH / 2, y=HEIGHT - 50)

    def handle_input(self, keys_pressed):
        if self.game_over or self.won:
            return
        dx = 0
        if keys_pressed[pygame.K_LEFT]:
            dx -= self.paddle.speed
        if keys_pressed[pygame.K_RIGHT]:
            dx += self.paddle.speed
        self.paddle.move(dx, WIDTH)

    def handle_keydown(self, key):
        if (self.game_over or self.won) and key == pygame.K_r:
            self.restart()

    def update(self):
        if self.game_over or self.won:
            return

        self.ball.update()
        self.ball.bounce_off_walls(WIDTH)

        if self.ball.get_rect().colliderect(self.paddle.get_rect()) and self.ball.vy > 0:
            self.ball.bounce_off_paddle(self.paddle.get_rect())

        for brick in self.bricks:
            if handle_ball_brick_collision(self.ball, brick):
                if brick.hit():
                    # Hits used up: remove the brick from play.
                    # Safe to mutate the list here because we break right after.
                    self.bricks.remove(brick)
                break

        if not any(b.breakable for b in self.bricks):
            self.won = True

        if self.ball.is_below(HEIGHT):
            self.lives -= 1
            if self.lives <= 0:
                self.game_over = True
            else:
                self._reset_ball()

    def draw(self, surface, font):
        from game import renderer
        renderer.draw_scene(surface, self.paddle, self.ball, self.bricks)
        renderer.draw_text(surface, font, f"Bricks left: {sum(b.breakable for b in self.bricks)}", (10, 10))
        renderer.draw_text(surface, font, f"Lives: {self.lives}", (520, 10))
        if self.game_over:
            renderer.draw_banner(surface, font, "GAME OVER", dy=-14)
            renderer.draw_banner(surface, font, "Press R to restart", dy=14)
        elif self.won:
            renderer.draw_banner(surface, font, "YOU WIN!", dy=-14)
            renderer.draw_banner(surface, font, "Press R to restart", dy=14)
