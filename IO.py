
def load_obj(file_path): #load obj file
    vertices = []
    texture_coords = []
    faces = []

    with open(file_path, 'r', encoding="utf-8") as file:
        for line in file:
            if line.startswith('v '):  # 정점
                vertices.append(tuple(map(float, line.strip().split()[1:4])))
            elif line.startswith('vt '):  # 텍스처 좌표
                texture_coords.append(tuple(map(float, line.strip().split()[1:3])))
            elif line.startswith('f '):  # 면
                face = [list(map(int, vert.split('/'))) for vert in line.strip().split()[1:]]
                faces.append(face)

    return vertices, texture_coords, faces