def coordinate_feature(mesh, edge_points):
  c1 = (mesh.vs[edge_points[:, 0]] + mesh.vs[edge_points[:,1]])/2
  c1 = np.max(c1, axis=1)
  c2 = ((mesh.vs[edge_points[:, 0]] + mesh.vs[edge_points[:,2]])/2)
  c2 = np.max(c2, axis=1)
  c3 = ((mesh.vs[edge_points[:, 1]] + mesh.vs[edge_points[:,2]])/2)
  c3 = np.max(c3, axis=1)
  c4 = ((mesh.vs[edge_points[:, 3]] + mesh.vs[edge_points[:,2]])/2)
  c4 = np.max(c4, axis=1)
  c5 = ((mesh.vs[edge_points[:, 1]] + mesh.vs[edge_points[:,3]])/2)
  c5 = np.max(c5, axis=1)
  A = [c1,c2,c3,c4,c5]
  B = np.array(A)
  print("B ", B.shape)
  return B

def extract_features(mesh):
    features = []
    edge_points = get_edge_points(mesh)
    set_edge_lengths(mesh, edge_points)
    with np.errstate(divide='raise'):
        try:
            # for extractor in [dihedral_angle, symmetric_opposite_angles, symmetric_ratios]:
            #     feature = extractor(mesh, edge_points)
            #     features.append(feature)
            # return np.concatenate(features, axis=0)
            feature = coordinate_feature(mesh, edge_points)
            print("feature shape", feature.shape)
            return feature

        except Exception as e:
            print(e)
            raise ValueError(mesh.filename, 'bad features')


        print("epoch: ", epoch)
        if(epoch==40):
          print("break at 40 epoch")
          break