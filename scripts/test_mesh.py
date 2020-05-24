import numpy as np
import compas
from compas.datastructures import Mesh
from compas_cgal._cgal import mesh


def main(v, f):
    V = np.asarray(v, dtype=np.float64)
    F = np.asarray(f, dtype=np.int32)

    mesh.mesh_test(V, F)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':

    from compas.utilities import print_profile

    m = Mesh.from_obj(compas.get('faces.obj'))
    v, f = m.to_vertices_and_faces()

    main = print_profile(main)

    main(v, f)
