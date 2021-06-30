import pygame
import os
import random
pygame.font.init()

WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rocket Game")

FPS = 60
FONT = pygame.font.SysFont('comicsans', 40)
SHIP_SPEED = 4
METEOR_SPEED = 7
SHOW_HITBOX = False

SPACESHIP_HEIGHT = 80
SPACESHIP_WIDTH = 60
SPACESHIP = pygame.image.load(os.path.join('resources', 'Spaceship.png'))  # works with every os
SPACESHIP = pygame.transform.scale(SPACESHIP, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT))

METEOR_HEIGHT = 50
METEOR_WIDTH = 50
METEOR = pygame.image.load(os.path.join('resources', 'Meteor.png'))
METEOR = pygame.transform.scale(METEOR, (METEOR_WIDTH, METEOR_HEIGHT))

BACKGROUND_HEIGHT = 500
BACKGROUND_WIDTH = 900
BACKGROUND = pygame.image.load(os.path.join('resources', 'Background.png'))
BACKGROUND = pygame.transform.scale(BACKGROUND, (BACKGROUND_WIDTH, BACKGROUND_HEIGHT))

COLLISION_EVENT = pygame.USEREVENT + 1


def draw(ship_rect, meteors, ship_health, gamestate):
    if gamestate == 1:
        draw_playing(ship_rect, meteors, ship_health)
    elif gamestate == 2:
        draw_loose()

def draw_playing(ship_rect, meteors, ship_health):
    WIN.fill((20, 20, 20))
    WIN.blit(BACKGROUND, (0, 0))
    if SHOW_HITBOX:
        pygame.draw.rect(WIN, (255, 255, 255), ship_rect)

    health_text = FONT.render("Health: " + str(ship_health), 1, (255, 20, 20))
    WIN.blit(health_text, (WIDTH - health_text.get_width() - 20, 20))
    WIN.blit(SPACESHIP, (ship_rect.x, ship_rect.y))

    for meteor in meteors:
        WIN.blit(METEOR, (meteor.x, meteor.y))



    pygame.display.update()


def draw_loose():
    text = FONT.render("You Died :C", 1, (255, 255, 255))
    WIN.blit(text, (WIDTH/2 - text.get_width() / 2, HEIGHT/2 - text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)
    main()

def handle_movement(keys_pressed, ship_rec):
    if keys_pressed[pygame.K_LEFT] and ship_rec.x - SHIP_SPEED > 0:
        ship_rec.x -= SHIP_SPEED
    if keys_pressed[pygame.K_RIGHT] and ship_rec.x + SHIP_SPEED < WIDTH - SPACESHIP_WIDTH:
        ship_rec.x += SHIP_SPEED
    if keys_pressed[pygame.K_UP] and ship_rec.y - SHIP_SPEED > 0:
        ship_rec.y -= SHIP_SPEED
    if keys_pressed[pygame.K_DOWN] and ship_rec.y + SHIP_SPEED < HEIGHT - SPACESHIP_HEIGHT:
        ship_rec.y += SHIP_SPEED


def handle_meteors(meteors, ship_rect):
    for meteor in meteors:
        meteor.y += METEOR_SPEED
        if ship_rect.colliderect(meteor):  # check collision
            pygame.event.post(pygame.event.Event(COLLISION_EVENT))
            meteors.remove(meteor)
        if meteor.y > HEIGHT or meteor.x > WIDTH or meteor.x < 0 - METEOR_WIDTH or meteor.y < 0 - METEOR_HEIGHT:
            meteors.remove(meteor)


def main():
    gamestate = 1
    meteors = []
    ship_health = 5
    ship_rect = pygame.Rect(WIDTH / 2 - SPACESHIP_WIDTH / 2, HEIGHT / 2 - SPACESHIP_HEIGHT / 2, SPACESHIP_WIDTH,
                            SPACESHIP_HEIGHT)
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == COLLISION_EVENT:
                ship_health -= 1
        if ship_health < 0:
            gamestate = 2

        if random.randint(0, 100) < 5:  # circa 1% of the time it generates a meteor
            meteors.append(pygame.Rect(random.randint(0, WIDTH), 0 - METEOR_HEIGHT, METEOR_WIDTH, METEOR_HEIGHT))

        handle_meteors(meteors, ship_rect)

        keys_pressed = pygame.key.get_pressed()
        handle_movement(keys_pressed, ship_rect)

        draw(ship_rect, meteors, ship_health, gamestate)
    pygame.quit()


if __name__ == "__main__":
    main()
