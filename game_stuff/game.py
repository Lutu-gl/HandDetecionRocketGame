import pygame
import os

WIDTH, HEIGHT = 900, 500
print(HEIGHT)
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rocket Game")

FPS = 60
SPEED = 4
SHOW_HITBOX = True

SPACESHIP_HEIGHT = 80
SPACESHIP_WIDTH = 60
SPACESHIP = pygame.image.load(os.path.join('resources', 'Spaceship.png')) #works with every os
SPACESHIP = pygame.transform.scale(SPACESHIP, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT))


def draw(ship_rect):
    WIN.fill((20, 20, 20))
    if SHOW_HITBOX:
        pygame.draw.rect(WIN, (255, 255, 255), ship_rect)
    WIN.blit(SPACESHIP, (ship_rect.x, ship_rect.y))

    pygame.display.update()

def handle_movement(keys_pressed, ship_rec):
    if keys_pressed[pygame.K_LEFT] and ship_rec.x - SPEED > 0:
        ship_rec.x -= SPEED
    if keys_pressed[pygame.K_RIGHT] and ship_rec.x + SPEED < WIDTH-SPACESHIP_WIDTH:
        ship_rec.x += SPEED
    if keys_pressed[pygame.K_UP] and ship_rec.y - SPEED > 0:
        ship_rec.y -= SPEED
    if keys_pressed[pygame.K_DOWN] and ship_rec.y + SPEED < HEIGHT-SPACESHIP_HEIGHT:
        ship_rec.y += SPEED

def main():
    ship_rect = pygame.Rect(WIDTH/2-SPACESHIP_WIDTH/2, HEIGHT/2-SPACESHIP_HEIGHT/2, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        keys_pressed = pygame.key.get_pressed()
        handle_movement(keys_pressed, ship_rect)

        draw(ship_rect)
    pygame.quit()


if __name__ == "__main__":
    main()