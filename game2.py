import pygame
import math

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ball in Rotating Octagon")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)

# Game State class to manage ball and octagon properties
class GameState:
    def __init__(self):
        self.ball_radius = 20
        self.ball_x, self.ball_y = WIDTH // 2, HEIGHT // 2
        self.ball_vx, self.ball_vy = 5, 0  # Initial velocity
        self.gravity = 0.5
        self.octagon_radius = 200
        self.octagon_center = (WIDTH // 2, HEIGHT // 2)
        self.angle = 0  # For rotation
        self.rotation_speed = 0.01  # radians per frame

clock = pygame.time.Clock()

def draw_octagon(surface, center, radius, angle):
    points = []
    for i in range(8):
        angle_i = angle + i * math.pi / 4
        x = center[0] + radius * math.cos(angle_i)
        y = center[1] + radius * math.sin(angle_i)
        points.append((x, y))
    pygame.draw.polygon(surface, WHITE, points, 2)

def main():
    game_state = GameState()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Clear the screen
        screen.fill(BLACK)

        # Update ball position
        game_state.ball_vy += game_state.gravity
        game_state.ball_x += game_state.ball_vx
        game_state.ball_y += game_state.ball_vy

        # Rotate octagon
        game_state.angle += game_state.rotation_speed

        # Check for collision with octagon sides
        ball_pos = pygame.math.Vector2(game_state.ball_x, game_state.ball_y)
        octagon_center_pos = pygame.math.Vector2(game_state.octagon_center)

        for i in range(8):
            angle_i = game_state.angle + i * math.pi / 4
            angle_next = game_state.angle + ((i + 1) % 8) * math.pi / 4
            p1 = pygame.math.Vector2(octagon_center_pos + pygame.math.Vector2(math.cos(angle_i), math.sin(angle_i)) * game_state.octagon_radius)
            p2 = pygame.math.Vector2(octagon_center_pos + pygame.math.Vector2(math.cos(angle_next), math.sin(angle_next)) * game_state.octagon_radius)

            # Vector from ball to p1
            line1 = p1 - ball_pos
            # Vector from ball to p2
            line2 = p2 - ball_pos

            # Check if ball is close enough to line segment
            if (abs(pygame.math.Vector2.cross(line1, line2)) < game_state.ball_radius * 10 and 
                line1.length() <= (p1 - p2).length() and 
                line2.length() <= (p1 - p2).length()):
                normal = (p2 - p1).normalize().rotate(90)
                dot = game_state.ball_vx * normal.x + game_state.ball_vy * normal.y
                game_state.ball_vx -= 2 * dot * normal.x
                game_state.ball_vy -= 2 * dot * normal.y
                # Adjust position slightly to prevent sticking
                ball_pos -= normal * (game_state.ball_radius - (ball_pos - p1).project(normal).length())

        # Keep ball within screen boundaries
        game_state.ball_x = max(game_state.ball_radius, min(WIDTH - game_state.ball_radius, game_state.ball_x))
        game_state.ball_y = max(game_state.ball_radius, min(HEIGHT - game_state.ball_radius, game_state.ball_y))

        # Draw the octagon
        draw_octagon(screen, game_state.octagon_center, game_state.octagon_radius, game_state.angle)

        # Draw ball
        pygame.draw.circle(screen, BLUE, (int(game_state.ball_x), int(game_state.ball_y)), game_state.ball_radius)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
