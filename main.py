import pygame
from IO import load_obj
import System

# pygame init
pygame.init()
screen = pygame.display.set_mode((1280, 720))  # HD resolution supported
clock = pygame.time.Clock()

scale = 500
x_offset, y_offset, z_offset = 0, 0, 1
x_box, y_box, z_box = 0, 0, 1
speed = 10

# under: Stelle Init
vertices, texture_coords, faces = load_obj("TrailBlazer/untitled.obj")
Stelle = System.Character()  # 25342 Polygons
Stelle.set_vtf(vertices, texture_coords, faces)
Stelle.set_isColliding(True)  # Stelle는 충돌 당하는 Polygon들이 존재하는 Obj

# under: Box Init
b_v, b_t, b_f = load_obj("TrailBlazer/box.obj")
Box = System.Character()
Box.set_vtf(b_v, b_t, b_f)
Box.set_isColliding(False)
Box.cal_AABB_init(scale)


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()

    keyEvent = pygame.key.get_pressed()
    if keyEvent[pygame.K_w]:
        y_offset -= speed
    if keyEvent[pygame.K_s]:
        y_offset += speed
    if keyEvent[pygame.K_a]:
        x_offset -= speed
    if keyEvent[pygame.K_d]:
        x_offset += speed
    if keyEvent[pygame.K_LEFT]:
        x_box -= speed
    if keyEvent[pygame.K_RIGHT]:
        x_box += speed
    if keyEvent[pygame.K_UP]:
        y_box -= speed
    if keyEvent[pygame.K_DOWN]:
        y_box += speed
    screen.fill((0, 0, 0))

    Box.set_offset(x_box, y_box, z_box)
    Box.cal_AABB_while(x_box, y_box, 0)

    Stelle.set_offset(x_offset, y_offset, z_offset)
    Stelle.set_collider_box(Box.collider_box)

    Stelle.render_obj(screen, scale, 1280, 720)
    Box.render_obj(screen, scale, 1280, 720)

    # Display camera status
    font = pygame.font.SysFont("Arial", 18)
    status_text = f"Stelle X: {x_offset}, Y: {y_offset}, Distance: {z_offset}"
    text_surface = font.render(status_text, True, (255, 255, 255))
    screen.blit(text_surface, (10, 10))

    pygame.display.update()
    clock.tick(60)

pygame.quit()