import mesh
import copy
from Edge import Edge
import numpy as np
def copy_mesh(mesh, data_path):
    mesh = mesh.HalfedgeMesh(data_path)
    vertices = copy.deepcopy(mesh.vertices)
    facets = copy.deepcopy(mesh.facets)
    return vertices, facets

def create_edge(vertex_index1, vertex_index2):
    vertex1 = vertices[vertex_index1].get_vertex()
    vertex2 = vertices[vertex_index2].get_vertex()
    edge = Edge(vertex1, vertex2)
    return edge

def get_coordinate(vertex_index):
    return vertices[vertex_index].get_vertex()

def sharedFace(my_edge, face_points):
    remote_points = [fp for fp in face_points if my_edge.vertices[0] != fp and my_edge.vertices[1] != fp]
    print("shared Face face_points ", face_points)
    print("my edge",my_edge)
    print("remote points are ", remote_points)
    return remote_points[0]
def isShareEdge(my_edge, facets):
    count = 0
    remote_point_list = []
    for face in facets:
        a = get_coordinate(face.a)
        b = get_coordinate(face.b)
        c = get_coordinate(face.c)
        face_points = [a,b,c]
        print(face_points)
        if my_edge.vertices[0] in face_points and my_edge.vertices[1] in face_points:
            remote_point_list.append(sharedFace(my_edge, face_points))
            count += 1
        if count == 2:
            print("shared edge", count)
            return remote_point_list
    if count == 1:
        print("boundary edge",count)
        return
    else:
        print("wrong count: ", count)
        return

def odd_shared_edge_vertex(edge, remote1, remote2):
    v = [0]*3
    for i in range(3):
        v[i] = 3.0/8.0 * (edge.vertices[0][i] + edge.vertices[1][i]) + 1.0/8.0 * (remote1[i] + remote2[i])
    return v

# def even_shared_edge_vertex():
#     v =

def loop_all_faces(vertices, facets):
    new_facets = []
    v_index = len(vertices)

    for face in facets:
        a = get_coordinate(face.a)
        b = get_coordinate(face.b)
        c = get_coordinate(face.c)
        edge1 = Edge(a,b)
        edge2 = Edge(b,c)
        edge3 = Edge(a,c)
        new_odd_vertices = []
        new_faces_per_triangle = []
        shared_edges = []

        for edge in [edge1, edge2, edge3]:
            if(isShareEdge(edge, facets)):
                shared_edges.append(edge)
                remote_points = isShareEdge(edge, facets) # two faces one point for each face
                print("remote - points list ", remote_points)
                if remote_points:
                    print("if remote_points")
                    print(edge.vertices[0])
                    print(edge.vertices[1])
                    print(remote_points[0])
                    print(remote_points[1])
                    new_odd_vertex = odd_shared_edge_vertex(edge, remote_points[0], remote_points[1])
                    print("new_odd_vertex", new_odd_vertex)
                    new_odd_vertices.append(new_odd_vertex)
                print('end of remote_points')
        mid_points = []

        if len(new_odd_vertices) == 1 and len(shared_edges) == 1:
            """
                shared_edges = [ab]
                vertex_on_face = c
            """

            for vertex_on_face in [a,b,c]:
                if vertex_on_face not in shared_edges:
                    # remote point
                    mid_point = 1/2 * (vertex_on_face + shared_edges.[0])
                    mid_points.append(mid_point)
                    new_faces_per_triangle.append([mid_points[0], shared_edges[0], new_odd_vertices[0]])

                    mid_point = 1 / 2 * (vertex_on_face + shared_edges[1])
                    mid_points.append(mid_point)
                    new_faces_per_triangle.append(mid_points[0], mid_points[1], vertex_on_face)

                    new_faces_per_triangle.append(mid_points[1],shared_edges[1], new_odd_vertices[1])
                    break
            print("new_faces_per_triangle", new_faces_per_triangle)
            break


vertices, facets = copy_mesh(mesh, "./tests/data/cube.off")
my_edge = create_edge(0,1)
print("here", my_edge.vertices[0], my_edge.vertices[1])

# print(isShareEdge(my_edge, facets))
loop_all_faces(vertices, facets)