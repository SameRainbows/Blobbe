import os
import random
import sys
import pygame

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(os.path.dirname(__file__))
    return os.path.join(base_path, relative_path)

pygame.init()

screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
speed = 6      

pygame.display.set_caption('Blobbe')
running = True
jumping = False

slime_image = pygame.image.load(resource_path('slime.png')).convert_alpha()
slime_image = pygame.transform.scale(slime_image, (200, 200))

pygame.display.set_icon(slime_image)

ground_image = pygame.image.load(resource_path('ground.png')).convert_alpha()
ground_image = pygame.transform.scale(ground_image, (1280, 200))

boulder_image = pygame.image.load(resource_path('boulder.png')).convert_alpha()
boulder_image = pygame.transform.scale(boulder_image, (100, 100))

slime_mask = pygame.mask.from_surface(slime_image)
ground_mask = pygame.mask.from_surface(ground_image)
boulder_mask = pygame.mask.from_surface(boulder_image)

def masks_collide(first_mask, first_rect, second_mask, second_rect):
    if not first_rect.colliderect(second_rect):
        return False

    offset = (second_rect.x - first_rect.x, second_rect.y - first_rect.y)
    return first_mask.overlap(second_mask, offset) is not None

slime_rect = slime_image.get_rect()
slime_rect.topright = (400,470)

ground_rect1 = ground_image.get_rect()
ground_rect1.topright = (1280, 600)

ground_rect2 = ground_image.get_rect()
ground_rect2.topright = (2540, 600)

boulder_rect1 = boulder_image.get_rect()
boulder_rect1.topright =  (1280, 500)

boulder_rect2 = boulder_image.get_rect()
boulder_rect2.topright =  (980, 500)

while running:
    # poll for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            # Check for SPECIFIC keys
            if event.key == pygame.K_SPACE:

                if not jumping:
                    y_velocity = -18
                    jumping = True
                


    screen.fill('light blue')



    ground_rect1.x -= speed
    ground_rect2.x -= speed

    boulder_rect1.x -= speed
    boulder_rect2.x -= speed

    if ground_rect1.right <= 0:
        ground_rect1.x = ground_rect2.right

    if ground_rect2.right <= 0:
        ground_rect2.x = ground_rect1.right

    if jumping:
        slime_rect.y += y_velocity
        y_velocity += 0.65   

        if y_velocity > 0:
            for ground_rect in (ground_rect1, ground_rect2):
                if masks_collide(slime_mask, slime_rect, ground_mask, ground_rect):
                    while masks_collide(slime_mask, slime_rect, ground_mask, ground_rect):
                        slime_rect.y -= 1
                    jumping = False
                    y_velocity = 0
                    break

    if boulder_rect1.x + boulder_rect1.width <= 0:
        boulder_rect1.topright = random.randint(700, 1440), 500

    if boulder_rect2.x + boulder_rect2.width <= 0:
            boulder_rect2.topright = 1800, 500

    if (masks_collide(slime_mask, slime_rect, boulder_mask, boulder_rect1)
            or masks_collide(slime_mask, slime_rect, boulder_mask, boulder_rect2)):
        running = False


    # RENDER

    screen.blit(slime_image, slime_rect)
    screen.blit(ground_image, ground_rect1)
    screen.blit(ground_image, ground_rect2)
    screen.blit(boulder_image, boulder_rect1)
    screen.blit(boulder_image, boulder_rect2)


    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()