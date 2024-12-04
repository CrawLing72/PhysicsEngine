
import pygame
import numpy as np

from IO import load_obj
from System import render_obj

pygame.init()
screen = pygame.display.set_mode((1280, 720)) # HD resolution supported
clock = pygame.time.Clock()

vertices, texture_coords, faces = load_obj("TrailBlazer/untitled.obj")
scale = 500
z_offset = 3

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()

    screen.fill((0, 0, 0))
    render_obj(screen, vertices, faces, scale, 1280, 720, z_offset)
    pygame.display.update()
    clock.tick(60)

pygame.quit()