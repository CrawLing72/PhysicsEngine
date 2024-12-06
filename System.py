import pygame
import math

from pygame.transform import scale


# under : collision related

def project_polygon_to_plane(vertices, plane):
    # 디버깅 출력

    # 데이터 검증
    if not all(isinstance(v, (list, tuple)) and len(v) == 3 for v in vertices):
        raise ValueError("Invalid vertices format. Expected list of 3D points.")

    if plane == "XY":
        return [(v[0], v[1]) for v in vertices]
    elif plane == "YZ":
        return [(v[1], v[2]) for v in vertices]
    elif plane == "ZX":
        return [(v[0], v[2]) for v in vertices]
    else:
        raise ValueError(f"Invalid plane: {plane}")


def aabb_collision(box1, box2):
    # box: (min_x, min_y, max_x, max_y)
    return (
            box1[0] <= box2[2] and box1[2] >= box2[0] and
            box1[1] <= box2[3] and box1[3] >= box2[1]
    )

def polygon_collision(vertices, collider_box):
    for plane in ["XY", "YZ", "ZX"]:
        projected_vertices = project_polygon_to_plane(vertices, plane)
        poly_min_x = min(p[0] for p in projected_vertices)
        poly_min_y = min(p[1] for p in projected_vertices)
        poly_max_x = max(p[0] for p in projected_vertices)
        poly_max_y = max(p[1] for p in projected_vertices)

        poly_aabb = (poly_min_x, poly_min_y, poly_max_x, poly_max_y)

        # 충돌 조건 수정: AABB가 완전히 포함되어야 충돌로 간주
        if not (
            collider_box[plane][0] <= poly_aabb[0] and
            collider_box[plane][1] <= poly_aabb[1] and
            collider_box[plane][2] >= poly_aabb[2] and
            collider_box[plane][3] >= poly_aabb[3]
        ):
            return False  # 하나라도 포함되지 않으면 충돌 아님
    return True  # 모든 평면에서 포함됨

def polygon_AABB_init(vertices):
    """ For Box Collision AABB Info Init."""
    temp_dict = {}
    for plane in ["XY", "YZ", "ZX"]:
        projected_vertices = project_polygon_to_plane(vertices, plane)
        poly_min_x = min(p[0] for p in projected_vertices)
        poly_min_y = min(p[1] for p in projected_vertices)
        poly_max_x = max(p[0] for p in projected_vertices)
        poly_max_y = max(p[1] for p in projected_vertices)
        temp_dict[plane] = poly_min_x, poly_min_y, poly_max_x, poly_max_y

    return temp_dict


def check_polygon_collision(_v, _c):
    vertices, collider_box = _v, _c
    return polygon_collision(vertices, collider_box)

"""---------------------------------------------------------------------------------------"""

class Character:
    def __init__(self):
        self.x_offset = 0
        self.y_offset = 0
        self.z_offset = 0

        self.vertices = []
        self.texture_coords = []
        self.faces = []

        self.collider_box = {}
        self.isColliding = False # 충돌 당하는 놈인가?

    def perspective_projection(self, vertex, screen_width, screen_height, scale, fov=60):
        # Z 안정화: z 값이 너무 작으면 최소값으로 설정
        z = max(vertex[2] + self.z_offset, 1e-5)

        # 화면 비율 및 FoV 계산
        f = 1 / math.tan(math.radians(fov) / 2)

        # 데카르트 좌표계에서 변환
        x_cartesian = (f * vertex[0] / z) * scale
        y_cartesian = (f * vertex[1] / z) * scale

        # 오프셋 추가
        x_cartesian += self.x_offset / z
        y_cartesian += self.y_offset / z

        # Pygame 좌표계로 변환 (y 값 반전)
        x_pygame = int(x_cartesian + screen_width // 2)
        y_pygame = int(-y_cartesian + screen_height // 2)

        return x_pygame, y_pygame

    def cal_original_coordination(self, vertex, scale):
        x = vertex[0] * scale + self.x_offset
        y = vertex[1] * scale + self.y_offset
        z = vertex[2] * scale + self.z_offset
        return x, y, z

    def render_obj(self, screen, scale, screen_width, screen_height):
        adjusted_scale = scale / max(self.z_offset + 1, 1e-5)  # Z축 안정화
        for face in self.faces:  # 폴리곤 단위로 작업
            general_points = [
                self.cal_original_coordination(self.vertices[vert[0] - 1], scale) for vert in face
            ]
            # Pygame 좌표계로 변환된 점들
            projected_points = [
                self.perspective_projection(self.vertices[vert[0] - 1], screen_width, screen_height, adjusted_scale)
                for vert in face
            ]

            # 충돌 여부 확인
            collision_results = check_polygon_collision(general_points, self.collider_box)
            if self.isColliding and collision_results:
                pygame.draw.polygon(screen, (255, 0, 0), projected_points, 1)
            else:
                pygame.draw.polygon(screen, (255, 255, 255), projected_points, 1)


    def set_offset(self, _x, _y, _z):
        self.x_offset = _x
        self.y_offset = _y
        self.z_offset = _z

    def set_vtf(self, _v, _t, _f):
        self.vertices = _v
        self.texture_coords = _t
        self.faces = _f

    def set_isColliding(self, isColliding):
        self.isColliding = isColliding

    def set_collider_box(self, collider_box):
        self.collider_box = collider_box

    def cal_AABB_init(self, scale):
        """AABB 정보 계산"""
        transformed_points = [
            self.cal_original_coordination(vertex, scale)
            for vertex in self.vertices
        ]

        min_x = min(point[0] for point in transformed_points)
        max_x = max(point[0] for point in transformed_points)
        min_y = min(point[1] for point in transformed_points)
        max_y = max(point[1] for point in transformed_points)
        min_z = min(point[2] for point in transformed_points)
        max_z = max(point[2] for point in transformed_points)

        self.collider_box = {
            "XY": (min_x, min_y, max_x, max_y),
            "YZ": (min_y, min_z, max_y, max_z),
            "ZX": (min_z, min_x, max_z, max_x),
        }

    def cal_AABB_while(self, dx, dy, dz):
        """Box의 이동량을 반영한 AABB 업데이트"""
        self.collider_box = {
            "XY": (
                self.collider_box["XY"][0] + dx,
                self.collider_box["XY"][1] + dy,
                self.collider_box["XY"][2] + dx,
                self.collider_box["XY"][3] + dy,
            ),
            "YZ": (
                self.collider_box["YZ"][0] + dy,
                self.collider_box["YZ"][1] + dz,
                self.collider_box["YZ"][2] + dy,
                self.collider_box["YZ"][3] + dz,
            ),
            "ZX": (
                self.collider_box["ZX"][0] + dz,
                self.collider_box["ZX"][1] + dx,
                self.collider_box["ZX"][2] + dz,
                self.collider_box["ZX"][3] + dx,
            ),
        }
