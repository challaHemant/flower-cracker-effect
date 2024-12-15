import pygame
import random
import math

# Window dimensions
WIDTH, HEIGHT = 800, 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

class Flower:
    def __init__(self):
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(HEIGHT // 2, HEIGHT)
        self.petal_count = random.randint(5, 15)
        self.petal_radius = random.uniform(10, 30)
        self.color = (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255))

    def draw(self, screen):
        for i in range(self.petal_count):
            angle = i * math.pi * 2 / self.petal_count
            petal_x = self.x + math.cos(angle) * self.petal_radius
            petal_y = self.y + math.sin(angle) * self.petal_radius
            pygame.draw.line(screen, self.color, (self.x, self.y), (petal_x, petal_y), 2)

    def update(self):
        self.petal_radius += 0.5
        if self.petal_radius > 50:
            return False
        return True

class Firework:
    def __init__(self):
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(0, HEIGHT // 2)
        self.particles = []
        self.exploded = False

    def draw(self, screen):
        if not self.exploded:
            pygame.draw.circle(screen, WHITE, (self.x, self.y), 2)
        for particle in self.particles:
            particle.draw(screen)

    def update(self):
        if not self.exploded:
            if self.y < HEIGHT // 2 - 50:
                self.explode()
            self.y += 2
        else:
            for particle in self.particles:
                particle.update()
                if not particle.alive:
                    self.particles.remove(particle)
            if not self.particles:
                return False
        return True

    def explode(self):
        self.exploded = True
        for _ in range(50):
            self.particles.append(Particle(self.x, self.y))

class Particle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vel_x = random.uniform(-2, 2)
        self.vel_y = random.uniform(-2, 2)
        self.color = (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255))
        self.alive = True
        self.life = 100

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), 2)

    def update(self):
        self.x += self.vel_x
        self.y += self.vel_y
        self.life -= 2
        if self.life <= 0:
            self.alive = False

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    flowers = [Flower() for _ in range(10)]
    fireworks = [Firework() for _ in range(5)]

    running = True
    start_time = pygame.time.get_ticks()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                flowers.append(Flower())
                fireworks.append(Firework())

        screen.fill(BLACK)

        # Update and draw flowers
        for flower in flowers[:]:
            if not flower.update():
                flowers.remove(flower)
            flower.draw(screen)

        # Update and draw fireworks
        for firework in fireworks[:]:
            if not firework.update():
                fireworks.remove(firework)
            firework.draw(screen)

        pygame.display.flip()
        clock.tick(60)

        # Check if 30 seconds have passed
        current_time = pygame.time.get_ticks()
        if (current_time - start_time) / 1000 > 30:
            running = False

    pygame.quit()

if __name__ == "__main__":
    main()
