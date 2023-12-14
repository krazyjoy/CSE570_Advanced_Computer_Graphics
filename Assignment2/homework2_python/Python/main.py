import mesh
import math
import numpy as np
from collections import defaultdict


class Edge:
    def __init__(self, vertex1, vertex2):
        self.vertices = (vertex1, vertex2)
        self.vertices = tuple(sorted(self.vertices))

    def __eq__(self, other):
        return self.vertices == other.vertices

    def __hash__(self):
        return hash(self.vertices)

    def __repr__(self):
        return f"Edge({self.vertices[0]}, {self.vertices[1]})"


# Example Usage:

# edge1 = Edge([0, 0, 0], [1, 1, 1])
# edge2 = Edge((0, 0, 0), (2, 2, 2))
# edge3 = Edge((0, 0, 0), (1, 1, 1))  # This will be considered equal to edge1


# def copy_mesh(mesh, data_path):
#     mesh = mesh.HalfedgeMesh(data_path)
#     vertices = copy.deepcopy(mesh.vertices)
#     facets = copy.deepcopy(mesh.facets)
#     return vertices, facets

def create_edge(vertex_index1, vertex_index2):
    vertex1 = vertices[vertex_index1].get_vertex()
    vertex2 = vertices[vertex_index2].get_vertex()
    edge = Edge(vertex1, vertex2)
    return edge


def get_coordinate(vertex_index):
    return vertices[vertex_index].get_vertex()


def sharedFace(my_edge, face_points):
    remote_points = [0] * 2
    # remote_points =
    for fp in face_points:
        if my_edge.vertices[0] != fp and my_edge.vertices[1] != fp:
            remote_points = fp
    # print("shared Face face_points ", face_points)
    # print("my edge",my_edge)
    # print("remote points are ", remote_points)
    return remote_points


def find_boundary_edges(mesh):
    boundary_edges = list()

    for half_edge in mesh.halfedges:
        if half_edge.opposite is None:
            boundary_edges.append(half_edge)

    return boundary_edges

def find_adjacent_facet_for_halfedge(edge):


    halfedge = mesh.get_halfedge(edge.vertices[0], edge.vertices[1])
    adjacent_facet = []

    adjacent_facet.append(halfedge.facet.index)
    adjacent_facet.append(halfedge.opposite.facet.index)
    print(adjacent_facet)
    return adjacent_facet

def get_interior_odd_vertex(edge, remote1, remote2):
    v0 = edge.vertices[0]
    v1 = remote1
    v2 = edge.vertices[1]
    v3 = remote2

    new_x = 3 / 8 * (v0[0] + v2[0]) + 1 / 8 * (v3[0] + v1[0])
    new_y = 3 / 8 * (v0[1] + v2[1]) + 1 / 8 * (v3[1] + v1[1])
    new_z = 3 / 8 * (v0[2] + v2[2]) + 1 / 8 * (v3[2] + v1[2])
    return [new_x, new_y, new_z]


def get_boundary_odd_vertex(edge):
    v0 = edge.vertices[0]
    v2 = edge.vertices[1]

    new_x = 1 / 2 * (v0[0] + v2[0])
    new_y = 1 / 2 * (v0[1] + v2[1])
    new_z = 1 / 2 * (v0[2] + v2[2])

    return [new_x, new_y, new_z]

def get_halfedge(v1, v2):

    for half_edge in mesh.halfedges:
        if half_edge.prev.vertex.index == v1 and half_edge.vertex.index == v2 \
                or half_edge.prev.vertex.index == v2 and half_edge.vertex.index == v1:
            # or half_edge.prev.vertex.index == v2 and half_edge.vertex.index == v1 \
            # or half_edge.vertex.index == v1 and half_edge.next.vertex.index == v2 \
            # or half_edge.vertex.index == v2 and half_edge.next.vertex.index == v1 \
            # or half_edge.next.vertex.index == v1 and half_edge.prev.vertex.index == v2 \
            # or half_edge.next.vertex.index == v2 and half_edge.prev.vertex.index == v1:
            return half_edge
        if half_edge.opposite:
            if half_edge.opposite.prev.vertex.index == v1 and half_edge.opposite.vertex.index == v2 \
                    or half_edge.opposite.prev.vertex.index == v2 and half_edge.opposite.vertex.index == v1:

                return half_edge.opposite

def match(shared_face_indices, face_indices):
    if shared_face_indices == [0,1]:
        return face_indices[0], face_indices[1]
    elif shared_face_indices == [0,2]:
        return face_indices[0], face_indices[2]
    elif shared_face_indices == [1,2]:
        return face_indices[1], face_indices[2]


def get_odd_vertice_and_new_facets(vertices, facets):
    new_facets = []
    new_vertices = []
    sub_vertice_dict = defaultdict(list)

    for vertex in vertices:
        new_vertices.append(vertex.get_vertex())

    for half_edge in mesh.halfedges:
        share_vertices = [half_edge.prev.vertex.index, half_edge.vertex.index]
        face_indices = [mesh.facets[half_edge.facet.index].a, mesh.facets[half_edge.facet.index].b, mesh.facets[half_edge.facet.index].c]
        shared_face_indices = [face_indices.index(share_vertices)]


         match(shared_face_indices, face_indices)



        a = get_coordinate(face_indices[0])
        b = get_coordinate(face_indices[1])
        c = get_coordinate(face_indices[2])

        edge1 = Edge(a, b)
        edge2 = Edge(b, c)
        edge3 = Edge(c, a)



        if half_edge not in boundary_edges:
            # find adjacent face
            a = half_edge.prev.vertex.index
            b = half_edge.vertex.index
            edge = Edge(a,b)
            adjacent_facets = [facet for facet in find_adjacent_facet_for_halfedge(edge) if facet != half_edge.opposite.facet.index][0]
            adjacent_facet_vertices = [mesh.facets[adjacent_facets].a, mesh.facets[adjacent_facets].b, mesh.facets[adjacent_facets].c]
            d = [vertex for vertex in adjacent_facet_vertices if vertex not in [a, b]][0]

            odd_vertex_ab = get_interior_odd_vertex(edge, get_coordinate(d), c)
        else:
            odd_vertex_ab = get_boundary_odd_vertex(edge)


        # Check if odd vertex repeat and create new face
        if odd_vertex_ab in new_vertices:
            index_ab = new_vertices.index(odd_vertex_ab)
        else:
            new_vertices.append(odd_vertex_ab)
            index_ab = new_vertices.index(odd_vertex_ab)

        if odd_vertex_bc in new_vertices:
            index_bc = new_vertices.index(odd_vertex_bc)
        else:
            new_vertices.append(odd_vertex_bc)
            index_bc = new_vertices.index(odd_vertex_bc)

        if odd_vertex_ca in new_vertices:
            index_ca = new_vertices.index(odd_vertex_ca)
        else:
            new_vertices.append(odd_vertex_ca)
            index_ca = new_vertices.index(odd_vertex_ca)

        new_face_0 = [face_indices[0], index_ab, index_ca]
        new_face_1 = [index_ab, face_indices[1], index_bc]
        new_face_2 = [index_bc, face_indices[2], index_ca]
        new_face_3 = [index_ab, index_bc, index_ca]

        # new_vertices.append(odd_vertex_ab)
        # new_vertices.append(odd_vertex_bc)
        # new_vertices.append(odd_vertex_ca)

        # new_face_0 = [face.a, len(new_vertices) - 3, len(new_vertices) - 1]
        # new_face_1 = [face.b, len(new_vertices) - 2, len(new_vertices) - 3]
        # new_face_2 = [face.c, len(new_vertices) - 1, len(new_vertices) - 2]
        # new_face_3 = [len(new_vertices) - 1, len(new_vertices) - 3, len(new_vertices) - 2]

        new_facets.append(new_face_0)
        new_facets.append(new_face_1)
        new_facets.append(new_face_2)
        new_facets.append(new_face_3)

    # new_facets = [[x + 1 for x in face] for face in new_facets]

    return new_vertices, new_facets


def calculate_neighbor(vertices, facets):
    neighbor_index = defaultdict(list)
    neighbor_num = {}

    for vertex in vertices:

        for f in facets:
            fff = [f.a, f.b, f.c]
            if vertex.index in fff:
                neighbor_num[vertex.index] = neighbor_num.get(vertex.index, 0) + 1
                for i in fff:
                    if vertex.index != i and i not in neighbor_index[vertex.index]:
                        neighbor_index[vertex.index].append(i)

    return neighbor_index, neighbor_num


def get_beta(neighbors_count):
    if neighbors_count == 3:
        return 3 / 16
    else:
        return (1.0 / neighbors_count) * (
                    5.0 / 8.0 - ((3.0 / 8.0) + (1.0 / 4.0) * math.cos(2 * math.pi / neighbors_count)) ** 2)


def update_old_vertice(vertices, facets):
    neighbor_index, neighbor_num = calculate_neighbor(vertices, facets)

    update_old = []

    for i in range(len(neighbor_num)):
        total_vi_x = 0
        total_vi_y = 0
        total_vi_z = 0

        if( neighbor_num[i] < 3):  # boundary but condition is wrong
            # a + b
            for j in neighbor_index[i]:
                total_vi_x += vertices[j].get_vertex()[0]
            for j in neighbor_index[i]:
                total_vi_y += vertices[j].get_vertex()[1]
            for j in neighbor_index[i]:
                total_vi_z += vertices[j].get_vertex()[2]

            # v = 3/8 * (a+b) + 1/8 * (c+d) where a,b shares edge, c,d are remote points
            v_update_x = (3.0 / 4.0) * vertices[i].get_vertex()[0] + (1.0 / 8.0) * total_vi_x
            v_update_y = (3.0 / 4.0) * vertices[i].get_vertex()[1] + (1.0 / 8.0) * total_vi_y
            v_update_z = (3.0 / 4.0) * vertices[i].get_vertex()[2] + (1.0 / 8.0) * total_vi_z

        else:
            for j in neighbor_index[i]:
                total_vi_x += get_beta(neighbor_num[i]) * vertices[j].get_vertex()[0]
            for j in neighbor_index[i]:
                total_vi_y += get_beta(neighbor_num[i]) * vertices[j].get_vertex()[1]
            for j in neighbor_index[i]:
                total_vi_z += get_beta(neighbor_num[i]) * vertices[j].get_vertex()[2]

            v_update_x = (1 - neighbor_num[i] * get_beta(neighbor_num[i])) * vertices[i].get_vertex()[0] + total_vi_x
            v_update_y = (1 - neighbor_num[i] * get_beta(neighbor_num[i])) * vertices[i].get_vertex()[1] + total_vi_y
            v_update_z = (1 - neighbor_num[i] * get_beta(neighbor_num[i])) * vertices[i].get_vertex()[2] + total_vi_z

        # for j in neighbor_index[i]:
        #     total_vi_x += get_beta(neighbor_num[i]) * vertices[j].get_vertex()[0]
        # for j in neighbor_index[i]:
        #     total_vi_y += get_beta(neighbor_num[i]) * vertices[j].get_vertex()[1]
        # for j in neighbor_index[i]:
        #     total_vi_z += get_beta(neighbor_num[i]) * vertices[j].get_vertex()[2]

        # v_update_x = (1 - neighbor_num[i] * get_beta(neighbor_num[i])) * vertices[i].get_vertex()[0] + total_vi_x
        # v_update_y = (1 - neighbor_num[i] * get_beta(neighbor_num[i])) * vertices[i].get_vertex()[1] + total_vi_y
        # v_update_z = (1 - neighbor_num[i] * get_beta(neighbor_num[i])) * vertices[i].get_vertex()[2] + total_vi_z

        # update_old.append([round(v_update_x, 3), round(v_update_y, 3), round(v_update_z, 3)])
        update_old.append([v_update_x, v_update_y, v_update_z])

    return update_old


def save_halfmesh_as_obj(all_vertex, new_facet, file_name):
    with open(file_name, 'w') as open_file:
        for vertex in all_vertex:
            x = vertex[0]
            y = vertex[1]
            z = vertex[2]
            open_file.write("v {} {} {}\n".format(x, y, z))

        for face in new_facet:
            f0 = face[0]
            f1 = face[1]
            f2 = face[2]
            open_file.write("f {} {} {}\n".format(f0 + 1, f1 + 1, f2 + 1))


data_path = 'tests/data/bunny.off'

# HalfedgeMesh
mesh = mesh.HalfedgeMesh(data_path)
#
# # Returns a list of Vertex type (in order of file)--similarly for halfedges,
# # and facets
# # mesh.vertices
#
# #
vertices, facets = mesh.vertices, mesh.facets
boundary_edges = find_boundary_edges(mesh)

print("length of boundary list")
print(len(boundary_edges))

print("length of total halfedges")
print(len(mesh.halfedges))




new_vertice, new_facets = get_odd_vertice_and_new_facets(vertices, facets)
# old_updated_vertice = update_old_vertice(vertices, facets)

for half_edge in mesh.halfedges:
    print(half_edge.prev.vertex.index)
    print(half_edge.vertex.index)
    print(half_edge.next.vertex.index)
    if(half_edge.opposite):
        print("has opposite\n")
        print(half_edge.opposite.prev.vertex.index)
        print(half_edge.opposite.vertex.index)
        print(half_edge.opposite.next.vertex.index)
    print(half_edge.facet.index)
    print(half_edge.index)
    print("------------------")

print("####################################")
