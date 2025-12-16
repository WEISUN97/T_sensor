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


# round corner
def round_corner(w1: float, w2: float, length: float, rotation=0, layer=(2, 0)):
    cs1 = gf.get_cross_section("strip", width=w1, layer=layer)
    cs2 = gf.get_cross_section("strip", width=w2, layer=layer)

    transition = gf.path.transition(cs1, cs2, width_type="parabolic")
    p = gf.path.straight(length, npoints=100)
    c = gf.path.extrude_transition(p, transition)
    c_component = gf.Component()
    (c_component << c).rotate(angle=rotation)
    return c_component


if __name__ == "__main__":
    c_component = round_corner(6, 2, 2, rotation=90)
    c_component.show()
