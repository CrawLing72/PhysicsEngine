import pygame

class Camera:
    def __init__(self, x=0, y=0, z=3):
        self.x_offset = x
        self.y_offset = y
        self.z_offset = z

    def move(self, dx=0, dy=0, dz=0):
        self.x_offset += dx
        self.y_offset += dy
        self.z_offset += dz


class Character:
    def __init__(self):
        self.x_offset = 0
        self.y_offset = 0
        self.z_offset = 0

        self.vertices = []
        self.texture_coords = []
        self.faces = []



    def perspective_projection(self, vertex, screen_width, screen_height, scale):
        z = vertex[2] + self.z_offset  # 카메라의 Z 오프셋
        if z == 0:
            z = 1e-5  # Z=0일 경우를 방지
        x = int((vertex[0] / z) * scale + screen_width // 2 + self.x_offset / z)
        y = int((-vertex[1] / z) * scale + screen_height // 2 + self.y_offset / z)
        return x, y

    def render_obj(self, screen, scale, screen_width, screen_height):
        adjusted_scale = scale / (self.z_offset + 1)
        for face in self.faces:
            points = [
                self.perspective_projection(self.vertices[vert[0] - 1], screen_width, screen_height, adjusted_scale) for vert in face]
            pygame.draw.polygon(screen, (255, 255, 255), points, 1)  # 면을 선으로 그리기

    def set_offset(self, _x, _y, _z):
        self.x_offset = _x
        self.y_offset = _y
        self.z_offset = _z

    def set_vtf(self, _v, _t, _f):
        self.vertices = _v
        self.texture_coords = _t
        self.faces = _f