import mesh
import math

# Assuming you have already loaded your mesh using the provided code
data_path = "./tests/data/cube.off"
mesh = mesh.HalfedgeMesh(data_path)


def calculate_new_vertex_interior(V0, V1, V2, V3):
    # Calculate the new vertex for an interior edge
    new_x = 3 / 8 * (V0[0] + V2[0]) + 1 / 8 * (V3[0] + V1[0])
    new_y = 3 / 8 * (V0[1] + V2[1]) + 1 / 8 * (V3[1] + V1[1])
    new_z = 3 / 8 * (V0[2] + V2[2]) + 1 / 8 * (V3[2] + V1[2])
    return [new_x, new_y, new_z]


def calculate_new_vertex_boundary(V1, V2):
    # Calculate the new vertex for a boundary edge
    new_x = 1 / 2 * (V1.x + V2.x)
    new_y = 1 / 2 * (V1.y + V2.y)
    new_z = 1 / 2 * (V1.z + V2.z)
    return mesh.Vertex(new_x, new_y, new_z)


new_vertices = []
share_edges = []
isolate_edges = []
for halfedge in mesh.halfedges:
    start_vertex = halfedge.vertex.index
    current_vertex = start_vertex
    while start_vertex != current_vertex:
        if halfedge.opposite:

            v0 = []
            v1 = []
            v2 = []
            v3 = []

            v0 = mesh.vertices[halfedge.facet.a].get_vertex()
            v1 = mesh.vertices[halfedge.facet.c].get_vertex()
            v2 = mesh.vertices[halfedge.facet.b].get_vertex()
            v3 = mesh.vertices[halfedge2.facet.c].get_vertex()
            new_vertices.append(calculate_new_vertex_interior(v0, v1, v2, v3))

            # new_vertices.append(new_vertex)
    # if not hasShareEdge:
    #     isolate_edge = [halfedge.prev.vertex.index, halfedge.vertex.index]
    #     isolate_edges.append(isolate_edge)

    #     new_vertex = 1/2 * (halfedge.prev.vertex.index + halfedge.vertex.index)
    #     new_vertices.append(new_vertex)
print(len(new_vertices))
# print("share_edge ... ")
# for share_edge in share_edges:
#     print(share_edge)
#     print("---------------------\n")

# print("isolate_edge ... ")
# for isolate_edge in isolate_edges:
#     print(isolate_edge)
#     print("---------------------\n")