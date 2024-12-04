
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

x_offset, y_offset = 0, 0

speed = 10;

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
        elif event.type == pygame.MOUSEWHEEL:
            z_offset += event.y * 0.1
    keyEvent = pygame.key.get_pressed()
    if keyEvent[pygame.K_w]:
        y_offset += speed
    elif keyEvent[pygame.K_s]:
        y_offset -= speed
    elif keyEvent[pygame.K_a]:
        x_offset += speed
    elif keyEvent[pygame.K_d]:
        x_offset -= speed


    screen.fill((0, 0, 0))
    render_obj(screen, vertices, faces, scale, 1280, 720, z_offset, x_offset, y_offset)
    pygame.display.update()
    clock.tick(60)

pygame.quit()