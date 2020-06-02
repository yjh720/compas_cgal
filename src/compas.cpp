#include <compas.h>

#include <pybind11/pybind11.h>

namespace py = pybind11;

// construct a CGAL surface mesh
// from vertices and faces
// contained in nx3 and fx3 eigen matrices
// using the Exact Predicates Exact Constructions Kernel
Mesh compas::mesh_from_vertices_and_faces(
    const compas::RowMatrixXd & V,
    const compas::RowMatrixXi & F)
{
    int v = V.rows();
    int f = F.rows();

    Mesh mesh;
    std::vector<Mesh::Vertex_index> index_descriptor(v);

    for (int i=0; i < v; i++) {
        index_descriptor[i] = mesh.add_vertex(Kernel::Point_3(V(i, 0), V(i, 1), V(i, 2)));
    }

    Mesh::Vertex_index a;
    Mesh::Vertex_index b;
    Mesh::Vertex_index c;

    for (int i=0; i < f; i++) {
        a = index_descriptor[F(i, 0)];
        b = index_descriptor[F(i, 1)];
        c = index_descriptor[F(i, 2)];
        mesh.add_face(a, b, c);
    }

    return mesh;
}

// construct a result
// from a CGAL surface mesh
compas::Result compas::result_from_mesh(Mesh mesh)
{
    int v = mesh.number_of_vertices();
    int f = mesh.number_of_faces();

    compas::Result R;
    compas::RowMatrixXd R_vertices(v, 3);
    compas::RowMatrixXi R_faces(f, 3);

    Mesh::Property_map<Mesh::Vertex_index, Kernel::Point_3> location = mesh.points();

    for (Mesh::Vertex_index vd : mesh.vertices()) {
        R_vertices(vd, 0) = (double) location[vd][0];
        R_vertices(vd, 1) = (double) location[vd][1];
        R_vertices(vd, 2) = (double) location[vd][2];
    }

    for (Mesh::Face_index fd : mesh.faces()) {
        int i = 0;
        for (Mesh::Vertex_index vd : vertices_around_face(mesh.halfedge(fd), mesh)) {
            R_faces(fd, i) = (int) vd;
            i++;
        }
    }

    R.vertices = R_vertices;
    R.faces = R_faces;

    return R;
}
