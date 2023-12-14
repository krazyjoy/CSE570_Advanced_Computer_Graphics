import mesh
import math
import numpy as np
from collections import defaultdict


def get_interior_odd_vertex(halfedge):
    
    a = vertices[halfedge.prev.vertex.index].get_vertex()
    b = vertices[halfedge.vertex.index].get_vertex()
    c = vertices[halfedge.next.vertex.index].get_vertex()
    d = vertices[halfedge.opposite.next.vertex.index].get_vertex()

    new_x = 3/8 * (a[0] + b[0]) + 1/8 * (c[0] + d[0])
    new_y = 3/8 * (a[1] + b[1]) + 1/8 * (c[1] + d[1])
    new_z = 3/8 * (a[2] + b[2]) + 1/8 * (c[2] + d[2])
    
    return [new_x, new_y, new_z]

def get_boundary_odd_vertex(halfedge):

    a = vertices[halfedge.prev.vertex.index].get_vertex()
    b = vertices[halfedge.vertex.index].get_vertex()

    new_x = 1/2 * (a[0] + b[0])
    new_y = 1/2 * (a[1] + b[1])
    new_z = 1/2 * (a[2] + b[2])
    
    return [new_x, new_y, new_z]

def get_odd_vertice_and_new_facets(mesh):
    
    vertices, facets = mesh.vertices, mesh.facets
    
    new_facets = []
    new_vertices = []

    for vertex in vertices:
        new_vertices.append(vertex.get_vertex())

    for face in facets:

        halfedge = face.halfedge
        
        face = halfedge.facet

        index_a = halfedge.vertex.index
        vertex_a = vertices[index_a].get_vertex()

        index_b = halfedge.next.vertex.index
        vertex_b = vertices[index_b].get_vertex()

        index_c = halfedge.next.next.vertex.index
        vertex_c = vertices[index_c].get_vertex()

        edge_ab = halfedge
        edge_bc = halfedge.next
        edge_ca = halfedge.next.next

        if edge_ab.opposite is not None:
            odd_vertex_ab = get_interior_odd_vertex(edge_ab)
        else:
            odd_vertex_ab = get_boundary_odd_vertex(edge_ab)

        if edge_bc.opposite is not None:
            odd_vertex_bc = get_interior_odd_vertex(edge_bc)
        else:
            odd_vertex_bc = get_boundary_odd_vertex(edge_bc)

        if edge_ca.opposite is not None:
            odd_vertex_ca = get_interior_odd_vertex(edge_ca)
        else:
            odd_vertex_ca = get_boundary_odd_vertex(edge_ca)


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
        

        new_face_0 = [face.a, index_ab, index_ca]
        new_face_1 = [index_ab, face.b, index_bc]
        new_face_2 = [index_bc, face.c, index_ca]
        new_face_3 = [index_ab, index_bc, index_ca]

        new_facets.append(new_face_0)
        new_facets.append(new_face_1)
        new_facets.append(new_face_2)
        new_facets.append(new_face_3)

    return new_vertices, new_facets

def get_beta(neighbors_count):
    if neighbors_count == 3:
        return 3/16
    else:
        return (1.0 / neighbors_count) * (5.0 / 8.0 - ((3.0 / 8.0) + (1.0 / 4.0) * math.cos(2 * math.pi / neighbors_count))** 2)

def traverse_halfedge_ring(vertex):

    start_half_edge = vertex.halfedge
    current_half_edge = start_half_edge
    neighbor_half_edges = []

    while True:
        # Non boundary
        if current_half_edge.opposite is not None:

            neighbor_half_edges.append(current_half_edge.opposite.vertex.index)
            current_half_edge = current_half_edge.opposite.prev
        
        # Boundary
        else:
            neighbor_half_edges.append(current_half_edge.prev.vertex.index)
            while current_half_edge.next.opposite.next.opposite is not None:
                current_half_edge = current_half_edge.next.opposite.next
            neighbor_half_edges.append(current_half_edge.next.opposite.next.vertex.index)
            break
 
        if current_half_edge == start_half_edge:
            break

    return neighbor_half_edges


def update_old_vertice(mesh):

    vertices, facets = mesh.vertices, mesh.facets

    update_old = []

    neighbor_vertice_dict = {}

    for vertex in vertices:
        neighbor_vertice_dict[vertex.index] = traverse_halfedge_ring(vertex)
    
    # print(neighbor_vertice_dict)

    for vertex in vertices:
        sum_vi_x = 0
        sum_vi_y = 0
        sum_vi_z = 0

        neighbor_num = len(neighbor_vertice_dict[vertex.index])

        # Boundary
        if neighbor_num < 3:
            for neighbor_id in neighbor_vertice_dict[vertex.index]:
                sum_vi_x += vertices[neighbor_id].get_vertex()[0]
                sum_vi_y += vertices[neighbor_id].get_vertex()[1]
                sum_vi_z += vertices[neighbor_id].get_vertex()[2]            
            
            v_update_x = (3.0 / 4.0) * vertex.get_vertex()[0] + (1.0 / 8.0) * sum_vi_x
            v_update_y = (3.0 / 4.0) * vertex.get_vertex()[1] + (1.0 / 8.0) * sum_vi_y
            v_update_z = (3.0 / 4.0) * vertex.get_vertex()[2] + (1.0 / 8.0) * sum_vi_z
        
        # Non-boundary
        else:
            for neighbor_id in neighbor_vertice_dict[vertex.index]:
                sum_vi_x += get_beta(neighbor_num) * vertices[neighbor_id].get_vertex()[0]
                sum_vi_y += get_beta(neighbor_num) * vertices[neighbor_id].get_vertex()[1]
                sum_vi_z += get_beta(neighbor_num) * vertices[neighbor_id].get_vertex()[2]

            v_update_x = (1 - neighbor_num * get_beta(neighbor_num))* vertex.get_vertex()[0] + sum_vi_x
            v_update_y = (1 - neighbor_num * get_beta(neighbor_num))* vertex.get_vertex()[1] + sum_vi_y
            v_update_z = (1 - neighbor_num * get_beta(neighbor_num))* vertex.get_vertex()[2] + sum_vi_z
            
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

def obj_to_off(obj_file_path, off_file_path):
    vertices = []
    faces = []

    with open(obj_file_path, 'r') as obj_file:
        for line in obj_file:
            if line.startswith('v '):
                parts = line.split()[1:]
                vertex = tuple(map(float, parts))
                vertices.append(vertex)
            elif line.startswith('f '):
                parts = line.split()[1:]
                face = tuple(int(part.split('/')[0]) - 1 for part in parts)
                faces.append(face)

    with open(off_file_path, 'w') as off_file:
        off_file.write('OFF\n')
        off_file.write(f'{len(vertices)} {len(faces)} 0\n')

        for vertex in vertices:
            off_file.write(f'{vertex[0]} {vertex[1]} {vertex[2]}\n')

        for face in faces:
            off_file.write(f'{len(face)} {" ".join(map(str, face))}\n')

def save_off_file(vertices, faces, file_path):
    with open(file_path, 'w') as off_file:
        off_file.write('OFF\n')
        off_file.write(f'{len(vertices)} {len(faces)} 0\n')

        # Write vertices
        for vertex in vertices:
            off_file.write(' '.join(str(coord) for coord in vertex) + '\n')

        # Write faces
        for face in faces:
            off_file.write(' '.join(str(index) for index in [len(face)] + list(face)) + '\n')


# # Teapot sub 1
data_path = 'tests/data/teapot.off'
mesh_teapot = mesh.HalfedgeMesh(data_path)
vertices, facets = mesh_teapot.vertices, mesh_teapot.facets
new_vertice, new_facets = get_odd_vertice_and_new_facets(mesh_teapot)
old_updated_vertice = update_old_vertice(mesh_teapot)
new_vertice[:(len(old_updated_vertice))] = old_updated_vertice
save_halfmesh_as_obj(new_vertice, new_facets, 'teapot_sub_1.obj')
save_off_file(new_vertice, new_facets, 'teapot_sub_1.off')

# Teapot sub 2
data_path = 'teapot_sub_1.off'
mesh_teapot = mesh.HalfedgeMesh(data_path)
vertices, facets = mesh_teapot.vertices, mesh_teapot.facets
new_vertice, new_facets = get_odd_vertice_and_new_facets(mesh_teapot)
old_updated_vertice = update_old_vertice(mesh_teapot)
new_vertice[:(len(old_updated_vertice))] = old_updated_vertice
save_halfmesh_as_obj(new_vertice, new_facets, 'teapot_sub_2.obj')
save_off_file(new_vertice, new_facets, 'teapot_sub_2.off')


# Bunny sub 1
data_path = 'tests/data/bunny.off'
mesh_bunny = mesh.HalfedgeMesh(data_path)
vertices, facets = mesh_bunny.vertices, mesh_bunny.facets
new_vertice, new_facets = get_odd_vertice_and_new_facets(mesh_bunny)
old_updated_vertice = update_old_vertice(mesh_bunny)
new_vertice[:(len(old_updated_vertice))] = old_updated_vertice
save_halfmesh_as_obj(new_vertice, new_facets, 'bunny_sub_1.obj')
save_off_file(new_vertice, new_facets, 'bunny_sub_1.off')

# Bunny sub 2
data_path = 'bunny_sub_1.off'
mesh_bunny = mesh.HalfedgeMesh(data_path)
vertices, facets = mesh_bunny.vertices, mesh_bunny.facets
new_vertice, new_facets = get_odd_vertice_and_new_facets(mesh_bunny)
old_updated_vertice = update_old_vertice(mesh_bunny)
new_vertice[:(len(old_updated_vertice))] = old_updated_vertice
save_halfmesh_as_obj(new_vertice, new_facets, 'bunny_sub_2.obj')
save_off_file(new_vertice, new_facets, 'bunny_sub_2.off')

