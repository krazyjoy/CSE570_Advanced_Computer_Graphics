import mesh

data_path = 'tests/data/cube.off'
mesh = mesh.HalfedgeMesh(data_path)
for vertex in mesh.vertices:
    print(vertex.index)
    if vertex.index ==1:
        print(vertex.get_vertex())