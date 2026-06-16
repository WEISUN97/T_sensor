import gdsfactory as gf


# create a polygon reference
def polygon(points):
    p = gf.kdb.DPolygon(points)
    return p


# create a region (unit: nm)
def region(p):
    r = gf.kdb.Region(p.to_itype(gf.kcl.dbu))
    return r


# Define a custom polynomial transition function from y1 -> y2, for t ∈ [0,1].
def polynomial(t: float, y1: float, y2: float) -> float:
    return (y2 - y1) * t**3 + y1


# round corner as a base of a beam
def round_corner(w1: float, w2: float, length: float, rotation=0, layer=(2, 0)):
    cs1 = gf.get_cross_section("strip", width=w1, layer=layer)
    cs2 = gf.get_cross_section("strip", width=w2, layer=layer)

    transition = gf.path.transition(cs1, cs2, width_type="parabolic")
    p = gf.path.straight(length, npoints=100)
    c = gf.path.extrude_transition(p, transition)
    c_component = gf.Component()
    (c_component << c).rotate(angle=rotation)
    return c_component


# round corner for two intersecting beams
def round_corner_intersect(radius=90, angle=2, layer=(2, 0)):
    c1 = gf.Component()

    c = gf.components.triangle(layer=layer)
    c2 = gf.Component()

    rinner = 1000  # 	The circle radius of inner corners (in database units).
    router = 1000  # 	The circle radius of outer corners (in database units).
    n = 300  # 	The number of points per full circle.

    # Round corners for one layer only.
    for p in c.get_polygons()[gf.get_layer(layer)]:
        p_round = p.round_corners(rinner, router, n)
        c2.add_polygon(p_round, gf.get_layer(layer))
    c1 << c2
    # c1 << c
    c1.show()


def round_inner_corner(
    c: gf.Component, inner_radius, outer_radius, layer=(9, 0)
) -> gf.Component:
    c_out = gf.Component()
    reg = c.get_region(layer=layer, merge=True).rounded_corners(
        r_inner=inner_radius * 1000, r_outer=outer_radius * 1000, n=64
    )
    c_out.add_polygon(reg, layer=layer)
    c_out.add_ref(
        c.extract(
            layers=[l for l in c.layers if gf.get_layer(l) != gf.get_layer(layer)]
        )
    )
    c_out.ports = c.ports
    return c_out


# b2 = block.get_region(layer=(9, 0))
# b3 = b2.rounded_corners(1e4,1e4,100)
# c = gf.Component()
# c.add_polygon(b3, layer=(9, 0))
# c.show()

if __name__ == "__main__":
    c_component = round_corner_intersect()
