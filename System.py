import pygame

def perspective_projection(vertex, screen_width, screen_height, scale, z_offset):
    z = vertex[2] + z_offset  # 카메라의 Z 오프셋
    if z == 0:
        z = 1e-5  # Z=0일 경우를 방지
    x = int((vertex[0] / z) * scale + screen_width // 2)
    y = int((-vertex[1] / z) * scale + screen_height // 2)
    return x, y


def render_obj(screen, vertices, faces, scale, screen_width, screen_height, z_offset):
    for face in faces:
        points = [perspective_projection(vertices[vert[0] - 1], screen_width, screen_height, scale, z_offset) for vert in face]
        pygame.draw.polygon(screen, (255, 255, 255), points, 1)  # 면을 선으로 그리기


def map_uv_to_texture(uv, texture_width, texture_height):
    u, v = uv
    x = int(u * texture_width)
    y = int((1 - v) * texture_height)  # v 좌표는 위에서 아래로 감소
    return x, y