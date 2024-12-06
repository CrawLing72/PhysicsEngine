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
Stelle.cal_AABB_init(scale)

# under: Box Init
b_v, b_t, b_f = load_obj("TrailBlazer/box.obj")
Box = System.Character()
Box.set_vtf(b_v, b_t, b_f)
Box.set_isColliding(False)
Box.cal_AABB_init(scale)

print(Stelle.collider_box)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()

    keyEvent = pygame.key.get_pressed()

    stelle_dx, stelle_dy, stelle_dz = 0, 0, 0
    box_dx, box_dy, box_dz = 0, 0, 0

    # Cartesian coordinate movement
    if keyEvent[pygame.K_w]:
        y_offset += speed  # Up in Cartesian coordinates
        stelle_dy = speed
    if keyEvent[pygame.K_s]:
        y_offset -= speed  # Down in Cartesian coordinates
        stelle_dy = -speed
    if keyEvent[pygame.K_a]:
        x_offset -= speed  # Left in Cartesian coordinates
        stelle_dx = -speed
    if keyEvent[pygame.K_d]:
        x_offset += speed  # Right in Cartesian coordinates
        stelle_dx = speed
    if keyEvent[pygame.K_LEFT]:
        x_box -= speed  # Box moves left
        box_dx = -speed
    if keyEvent[pygame.K_RIGHT]:
        x_box += speed  # Box moves right
        box_dx = speed
    if keyEvent[pygame.K_UP]:
        y_box += speed  # Box moves up
        box_dy = speed
    if keyEvent[pygame.K_DOWN]:
        y_box -= speed  # Box moves down
        box_dy = -speed

    # AABB Initialization debug
    if keyEvent[pygame.K_SPACE]:
        Stelle.cal_AABB_init(scale)
        print("Stelle: ")
        print(Stelle.collider_box)
        print("Box: ")
        print(Box.collider_box)

    screen.fill((0, 0, 0))

    # Update offsets
    Box.set_offset(x_box, y_box, z_box)
    Box.cal_AABB_while(box_dx, box_dy, box_dz)

    Stelle.set_offset(x_offset, y_offset, z_offset)
    Stelle.set_collider_box(Box.collider_box)

    # Render objects
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