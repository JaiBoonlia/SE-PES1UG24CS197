"""
collision: ball-vs-brick collision handling.
"""


def handle_ball_brick_collision(ball, brick):
    """
    If the ball overlaps the brick, bounce it off and return True.

    The bounce axis is chosen from the smaller overlap (side hit vs
    top/bottom hit) and the ball is pushed out of the brick, so one
    touch can never count as several hits on multi-hit bricks.
    """
    ball_rect = ball.get_rect()
    brick_rect = brick.get_rect()
    if not ball_rect.colliderect(brick_rect):
        return False

    overlap_x = min(ball_rect.right, brick_rect.right) - max(ball_rect.left, brick_rect.left)
    overlap_y = min(ball_rect.bottom, brick_rect.bottom) - max(ball_rect.top, brick_rect.top)

    if overlap_x < overlap_y:
        # Side hit: bounce horizontally, away from the brick's centre.
        if ball.x < brick_rect.centerx:
            ball.x -= overlap_x
            ball.vx = -abs(ball.vx)
        else:
            ball.x += overlap_x
            ball.vx = abs(ball.vx)
    else:
        # Top/bottom hit: bounce vertically, away from the brick's centre.
        if ball.y < brick_rect.centery:
            ball.y -= overlap_y
            ball.vy = -abs(ball.vy)
        else:
            ball.y += overlap_y
            ball.vy = abs(ball.vy)
    return True
