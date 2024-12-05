import pygame
from IO import load_obj
import System

# pygame init
pygame.init()
screen = pygame.display.set_mode((1280, 720)) # HD resolution supported
clock = pygame.time.Clock()

# under : Stelle Init.
vertices, texture_coords, faces = load_obj("TrailBlazer/untitled.obj")
Stelle = System.Character()
Stelle.set_vtf(vertices, texture_coords, faces)

# under : bullet init.
vertices_2, texture_coords_2, faces_2 = load_obj("TrailBlazer/untitled.obj")
Box = System.Character()
Box.set_vtf(vertices_2, texture_coords_2, faces_2)

# camera init.
camera = System.Camera()

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
            camera.move(dz=event.y * 0.1)

    keyEvent = pygame.key.get_pressed()
    if keyEvent[pygame.K_w]:
        camera.move(dy=speed)
    if keyEvent[pygame.K_s]:
        camera.move(dy=-speed)
    if keyEvent[pygame.K_a]:
        camera.move(dx=speed)
    if keyEvent[pygame.K_d]:
        camera.move(dx=-speed)

    screen.fill((0, 0, 0))
    Stelle.set_offset(camera.x_offset, camera.y_offset, camera.z_offset)
    Stelle.render_obj(screen, scale, 1280, 720)

    Box.set_offset(camera.x_offset, camera.y_offset, camera.z_offset)
    Box.render_obj(screen, scale, 1280, 720)

    # Display camera status
    font = pygame.font.SysFont("Arial", 18)
    status_text = f"X: {camera.x_offset}, Y: {camera.y_offset}, Distance: {camera.z_offset}"
    text_surface = font.render(status_text, True, (255, 255, 255))
    screen.blit(text_surface, (10, 10))

    pygame.display.update()
    clock.tick(60)

pygame.quit()