import pygame
import os
import random
import numpy as np
import cv2

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
SPACESHIP = pygame.image.load(os.path.join('game_stuff', 'resources', 'Spaceship.png'))  # works with every os
SPACESHIP = pygame.transform.scale(SPACESHIP, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT))

METEOR_HEIGHT = 50
METEOR_WIDTH = 50
METEOR = pygame.image.load(os.path.join('game_stuff', 'resources', 'Meteor.png'))
METEOR = pygame.transform.scale(METEOR, (METEOR_WIDTH, METEOR_HEIGHT))

BACKGROUND_HEIGHT = 500
BACKGROUND_WIDTH = 900
BACKGROUND = pygame.image.load(os.path.join('game_stuff', 'resources', 'Background.png'))
BACKGROUND = pygame.transform.scale(BACKGROUND, (BACKGROUND_WIDTH, BACKGROUND_HEIGHT))

COLLISION_EVENT = pygame.USEREVENT + 1

#CAPTURE = cv2.VideoCapture(os.path.join('color_detection', 'vid.mp4'))
CAPTURE = cv2.VideoCapture(0)

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
    x = get_vid_input()[0]
    y = get_vid_input()[1]
    print('-_-: ' + str(x) + str(y))
    ship_rec.x = x
    ship_rec.y = y

def get_vid_input():
    ret, frame = CAPTURE.read()
    width = int(CAPTURE.get(3))
    height = int(CAPTURE.get(4))

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_bound = np.array([80, 50, 50])  # 80 50 50                 #Trying to get the right color (in this case blue)
    upper_bound = np.array([80 + 40, 255, 255])  # 80+40 255 255

    mask = cv2.inRange(hsv, lower_bound, upper_bound)  # mask between lower and upper bound
    result = cv2.bitwise_and(frame, frame, mask=mask)

    points = cv2.findNonZero(mask)
    resImage = [640, 480]  # not needed
    resScreen = [1920, 1080]
    try:
        avg = np.mean(points,
                      axis=0)  # for example when there are no points, the "points" array is None. When its none np.mean does't work
    except:
        return 0, 0

    # pointInScreen = ((resScreen[0] / resImage[0]) * avg[0][0], (resScreen[1] / resImage[1]) * avg[0][1]) #not needed right now
    # res = cv2.circle(res, (int(pointInScreen[0]),int(pointInScreen[1])), 10, (0, 0, 255), -1)

    result = cv2.circle(result, (int(avg[0][0]), int(avg[0][1])), 10, (0, 0, 255), -1)
    print('x=' + str(avg[0][0]) + ' y=' + str(avg[0][1]))

    cv2.imshow("videonormal", frame)
    cv2.imshow("videohsv", hsv)
    cv2.imshow("mask", mask)
    cv2.imshow("result", result)
    if cv2.waitKey(1) == ord('q'):
        pass
    if cv2.waitKey(1) == ord('p'):
        c = c + 1
        print(c)
    if cv2.waitKey(1) == ord('t'):
        flag = True
    return avg[0][0], avg[0][1]

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
                CAPTURE.release()
                cv2.destroyAllWindows()
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
