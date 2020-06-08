from compas.geometry import Point
from compas.geometry import Box
from compas.geometry import Sphere
from compas.geometry import Polyline
from compas.datastructures import Mesh

from compas_viewers.objectviewer import ObjectViewer

from compas_cgal.intersections import intersection_mesh_mesh
from compas_cgal.meshing import remesh

# ==============================================================================
# Make a box and a sphere
# ==============================================================================

box = Box.from_width_height_depth(2, 2, 2)
box = Mesh.from_shape(box)
box.quads_to_triangles()

A = box.to_vertices_and_faces()

sphere = Sphere(Point(1, 1, 1), 1)
sphere = Mesh.from_shape(sphere, u=30, v=30)
sphere.quads_to_triangles()

B = sphere.to_vertices_and_faces()

# ==============================================================================
# Remesh the sphere
# ==============================================================================

B = remesh(B, 0.3, 10)

# ==============================================================================
# Compute the intersections
# ==============================================================================

pointsets = intersection_mesh_mesh(A, B)

# ==============================================================================
# Process output
# ==============================================================================

polylines = []
for points in pointsets:
    points = [Point(*point) for point in points]
    polyline = Polyline(points)
    polylines.append(polyline)

# ==============================================================================
# Visualize
# ==============================================================================

# @li todo: increase thickness of intersection polyline independently
# @li todo: visualize polyline/intersection points
# @li perhaps the root scene element should not be explicitly mentioned in the object manager. it wastes a level of indentation...

viewer = ObjectViewer()
viewer.view.use_shaders = False

viewer.add(Mesh.from_vertices_and_faces(*A), settings={'color': '#ff0000'})
viewer.add(Mesh.from_vertices_and_faces(*B), settings={'color': '#00ff00'})

for polyline in polylines:
    viewer.add(polyline, settings={'color': '#0000ff'})

viewer.update()
viewer.show()
