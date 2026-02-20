import pygame
import random
import sys

pygame.init()

# ---------------- SCREEN ----------------
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bike Racing Game")
clock = pygame.time.Clock()

# ---------------- COLORS ----------------
BLACK = (0, 0, 0)
GRAY = (110, 110, 110)
YELLOW = (255, 220, 0)
RED = (200, 40, 40)
BLUE = (60, 90, 200)
WHITE = (255, 255, 255)

# ---------------- FONTS ----------------
FONT = pygame.font.SysFont(None, 36)
BIG_FONT = pygame.font.SysFont(None, 64)

# ---------------- ROAD ----------------
ROAD_WIDTH = 300
ROAD_X = (WIDTH - ROAD_WIDTH) // 2
LINE_HEIGHT = 40
LINE_GAP = 30
line_y = 0

# ---------------- PHYSICS ----------------
ACCELERATION = 0.25
MAX_SPEED = 9
FRICTION = 0.04
STEER_SPEED = 6

# ---------------- BIKE ----------------
class Bike:
    def __init__(self):
        self.x = WIDTH // 2
        self.y = HEIGHT - 130
        self.speed = 0
        self.angle = 0

        self.base_image = pygame.Surface((40, 90), pygame.SRCALPHA)
        self._draw_bike(self.base_image)
        self.image = self.base_image
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def _draw_bike(self, surf):
        pygame.draw.circle(surf, BLACK, (20, 75), 10)
        pygame.draw.circle(surf, BLACK, (20, 15), 10)
        pygame.draw.line(surf, BLACK, (20, 15), (20, 75), 4)
        pygame.draw.ellipse(surf, RED, (8, 35, 24, 22))
        pygame.draw.rect(surf, (120, 0, 0), (10, 25, 20, 10), border_radius=4)
        pygame.draw.line(surf, BLACK, (5, 10), (35, 10), 3)

    def update(self, keys):
        if keys[pygame.K_UP]:
            self.speed = min(self.speed + ACCELERATION, MAX_SPEED)
        else:
            self.speed *= (1 - FRICTION)

        if keys[pygame.K_LEFT]:
            self.x -= STEER_SPEED
            self.angle = min(self.angle + 3, 20)
        elif keys[pygame.K_RIGHT]:
            self.x += STEER_SPEED
            self.angle = max(self.angle - 3, -20)
        else:
            self.angle *= 0.85

        self.x = max(ROAD_X + 20, min(self.x, ROAD_X + ROAD_WIDTH - 20))

        self.image = pygame.transform.rotate(self.base_image, self.angle)
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def draw(self):
        screen.blit(self.image, self.rect)

# ---------------- ENEMY CAR ----------------
class EnemyCar:
    def __init__(self):
        self.width = 45
        self.height = 80
        self.x = random.randint(ROAD_X + 10, ROAD_X + ROAD_WIDTH - self.width - 10)
        self.y = -self.height

    def update(self, speed):
        self.y += speed + 6

    def draw(self):
        pygame.draw.rect(screen, BLUE, (self.x, self.y, self.width, self.height), border_radius=6)
        pygame.draw.rect(screen, WHITE, (self.x + 8, self.y + 12, self.width - 16, 18), border_radius=4)

    def rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

# ---------------- ROAD ----------------
def draw_road():
    global line_y
    pygame.draw.rect(screen, GRAY, (ROAD_X, 0, ROAD_WIDTH, HEIGHT))

    line_y += 10
    if line_y > LINE_HEIGHT + LINE_GAP:
        line_y = 0

    y = -LINE_HEIGHT
    while y < HEIGHT:
        pygame.draw.rect(screen, YELLOW, (WIDTH // 2 - 5, y + line_y, 10, LINE_HEIGHT))
        y += LINE_HEIGHT + LINE_GAP

# ---------------- GAME DATA ----------------
bike = Bike()
enemies = []
spawn_timer = 0
score = 0
game_over = False

# ---------------- MAIN LOOP ----------------
running = True
while running:
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:   # Q = QUIT
                running = False

            if game_over and event.key == pygame.K_r:
                bike = Bike()
                enemies.clear()
                spawn_timer = 0
                score = 0
                game_over = False

    if not game_over:
        draw_road()
        keys = pygame.key.get_pressed()
        bike.update(keys)

        spawn_timer += 1
        if spawn_timer > 70:
            enemies.append(EnemyCar())
            spawn_timer = 0

        for car in enemies[:]:
            car.update(bike.speed)

            if car.y > HEIGHT:
                enemies.remove(car)
                score += 1

            if bike.rect.colliderect(car.rect()):
                game_over = True

        bike.draw()
        for car in enemies:
            car.draw()

        screen.blit(FONT.render(f"Score: {score}", True, WHITE), (10, 10))

    else:
        screen.blit(BIG_FONT.render("GAME OVER", True, RED),
                    (WIDTH // 2 - 160, HEIGHT // 2 - 40))
        screen.blit(FONT.render("Press R to Restart | Q to Quit", True, WHITE),
                    (WIDTH // 2 - 180, HEIGHT // 2 + 20))

    pygame.display.update()
    clock.tick(60)

pygame.quit()
sys.exit()