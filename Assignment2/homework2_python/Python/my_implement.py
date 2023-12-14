import numpy as np
import mesh

def write_off(vertices_list, faces_list, filename):
    with open(filename, "w") as f:
        for vertex in vertices_list:
            f.write("v {} {} {} \n".format(vertex[0], vertex[1], vertex[2]))
        for face in faces_list:
            f.write("f {} {} {} \n".format(face[0], face[1], face[2]))

def get_vertex_points(vertex_index):
    return mesh.vertices[vertex_index].get_vertex()
def loop_subdivision(vertices, faces):
    new_vertices = []
    new_faces = []

    # Rule 1: Compute new positions for existing vertices
    for v_index in range(len(vertices)):
        print("v_index is ", v_index)
        valence = 0
        average_neighbor = np.zeros(3)
        neighbor_set = set()

        for face in faces:
            if v_index in face:

                valence += 1
                for neighbor_index in face:
                    if neighbor_index != v_index and neighbor_index not in neighbor_set:
                        neighbor_set.add(neighbor_index)

                        print("{} neighbors are {}".format(v_index, neighbor_index))
                        neighbor_points = get_vertex_points(neighbor_index)
                        average_neighbor += neighbor_points
                        print("current average neighbor value is {}".format(average_neighbor))

        if valence == 6:
            beta = 3/16
        else:
            beta = 3/(8*valence)

        vertex = np.array(get_vertex_points(v_index))

        new_position = (1 - valence*beta) * vertex + beta * average_neighbor

        new_vertices.append(new_position)

    # Rule 2: Compute new positions for new vertices
    edge_midpoints = {}
    for face in faces:
        for i in range(3):
            v1, v2 = sorted([face[i], face[(i+1)%3]])

            if (v1, v2) not in edge_midpoints or (v2, v1) not in edge_midpoints:
                edge_midpoint = (v1 + v2) / 2
                edge_midpoints[(v1, v2)] = edge_midpoint
                # print("edge_midpoints([{},{})] is {}".format(v1, v2, edge_midpoint))

    for face in faces:
        v1, v2, v3 = face
        midpoints = [edge_midpoints[tuple(sorted([v1, v2]))],
                     edge_midpoints[tuple(sorted([v2, v3]))],
                     edge_midpoints[tuple(sorted([v3, v1]))]]

        print("midpoints for face are ".format(midpoints))
        old_points1 = np.array(get_vertex_points(v1))
        old_points2 = np.array(get_vertex_points(v2))
        old_points3 = np.array(get_vertex_points(v3))
        print("old point 1", old_points1)
        print("old point 2", old_points2)
        print("old point 3", old_points3)
        print((old_points1 + old_points2 + old_points3) / 3)
        new_vertices.append((old_points1 + old_points2 + old_points3) / 3)

        new_vertices.extend(midpoints)

        new_faces.append([v1, len(vertices) + len(midpoints) - 3, len(vertices) + len(midpoints) - 2])
        new_faces.append([v2, len(vertices) + len(midpoints) - 2, len(vertices) + len(midpoints) - 1])
        new_faces.append([v3, len(vertices) + len(midpoints) - 1, len(vertices) + len(midpoints) - 3])
        new_faces.append([len(vertices) + len(midpoints) - 3, len(vertices) + len(midpoints) - 2, len(vertices) + len(midpoints) - 1])

    return new_vertices, new_faces




def calculate_new_points(vertex, n , beta, gamma):
    # new_vertex = (1 - n * beta - gamma) * vertex
    new_vertex = [0]*3
    for i in range(len(vertex)):
        new_vertex[i] = (1 - n * beta - gamma) * vertex[i]
    return new_vertex


def get_face_points(face_obj):
    a_point = index_2_point(face_obj.a)
    b_point = index_2_point(face_obj.b)
    c_point = index_2_point(face_obj.c)

    face_points = [a_point, b_point, c_point]
    return face_points
def index_2_point(vertex_index):
    coordinates = mesh.vertices[vertex_index].get_vertex()
    return coordinates
def get_neighbors(vertex_index, vertices, faces):
    neighbors = []
    for face in faces:
        if vertex_index in face: # find the face contains vertex
            for v in face: # neighbor vertices
                if v != vertex_index and vertices[v] not in neighbors:
                    neighbors.append(vertices[v])
    print("length of neighbors: ", len(neighbors))
    return neighbors

# Example usage
# Assuming you have loaded vertices and faces from your bunny mesh file
# vertices, faces = load_bunny_mesh()
data_path = "./tests/data/cube.off"
mesh = mesh.HalfedgeMesh(data_path)
num_iterations = 1


vertices = []
for vertex in mesh.vertices:
    vertex_coordinates = vertex.get_vertex()
    vertices.append(vertex_coordinates)

print(vertices)

#
faces = []
for face in mesh.facets:
    face_points = [face.a, face.b, face.c]
    faces.append(face_points)
print(faces)
for i in range(num_iterations):
    new_vertices, new_faces = loop_subdivision(vertices, faces)
    print("------------------vertices---------------------------\n\n")
    print(new_vertices)
    print("------------------faces--------------------------\n\n")
    print(new_faces)

write_off(new_vertices, new_vertices, "my_implement")

"""
import numpy as np

def compute_odd_points(vertices, faces):
    odd_points = np.zeros_like(vertices)
    edge_points = {}

    for face in faces:
        for i in range(3):
            v1, v2 = sorted([face[i], face[(i+1)%3]])
            edge_points[(v1, v2)] = edge_points.get((v1, v2), []) + [face[(i+2)%3]]

    for edge, neighbors in edge_points.items():
        n = len(neighbors)
        Q = sum(vertices[v] for v in neighbors) / n
        R = 3/8 * (vertices[edge[0]] + vertices[edge[1]]) + 1/8 * Q
        odd_points[edge[0]] = R

    return odd_points

def compute_even_points(vertices, faces, odd_points):
    even_points = np.zeros_like(vertices)

    for i, vertex in enumerate(vertices):
        neighbors = []
        for face in faces:
            if i in face:
                neighbors.extend([v for v in face if v != i])

        n = len(neighbors)
        beta = 3/16 if n == 3 else 3/(8*n)
        Q = sum(vertices[v] for v in neighbors) / n
        odd_neighbors = [odd_points[v] for v in neighbors]
        even_points[i] = (1 - n * beta) * vertex + beta * Q + beta * sum(odd_neighbors)

    return even_points

def loop_subdivision(vertices, faces, iterations):
    for _ in range(iterations):
        odd_points = compute_odd_points(vertices, faces)
        even_points = compute_even_points(vertices, faces, odd_points)
        vertices = np.vstack((even_points, odd_points))
        faces = []

        for face in faces:
            a, b, c = [v for v in face]
            ab, bc, ca = len(vertices) + a, len(vertices) + b, len(vertices) + c
            faces.extend([[a, ab, ca], [b, bc, ab], [c, ca, bc], [ca, ab, bc]])

    return vertices, faces

# Assuming 'vertices' is a numpy array of shape (N, 3)
# and 'faces' is a list of lists where each inner list contains vertex indices forming a face

# Example Usage
# vertices, faces = loop_subdivision(vertices, faces, iterations=3)

"""