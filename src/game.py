import pygame


def check_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return running(False)
