import mesh

def find_adjacent_faces(face):
    adjacent_faces = []
    start_edge = face.any_half_edge  # Choose any half-edge to start with

    current_edge = start_edge
    while True:
        twin_edge = current_edge.twin
        if twin_edge is not None and twin_edge.face is not face:
            adjacent_faces.append(twin_edge.face)

        next_edge = current_edge.next
        if next_edge is start_edge:
            break
        current_edge = next_edge

    return adjacent_faces


def find_boundary_edges(mesh):
    boundary_edges = []

    for half_edge in mesh.half_edges:
        if half_edge.twin is None:
            boundary_edges.append(half_edge)

    return boundary_edges
