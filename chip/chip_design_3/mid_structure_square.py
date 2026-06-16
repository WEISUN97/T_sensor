import gdsfactory as gf
from gdsfactory.generic_tech import get_generic_pdk
import sys

sys.path.append("/Users/bubble/Desktop/Project/T_sensor/T_sensor")
from Tools.geo_trans import round_corner

PDK = get_generic_pdk()
PDK.activate()


def single_spring_path_singleside(
    spring_num=2, total_length=250, horizontal_length=20, vertical_length=6, radius=5
):
    # springs
    P = gf.Path()
    # vertical paths
    vertical_path = (
        total_length - (spring_num * (vertical_length + 2 * radius) + 2 * radius)
    ) / 2
    P.append(gf.path.straight(length=vertical_path))

    for i in range(spring_num):
        if i % 2 == 0:
            if i == 0:
                P.append(gf.path.arc(radius=radius, angle=90))
                P.append(gf.path.straight(length=horizontal_length))
            else:
                P.append(gf.path.straight(length=horizontal_length + radius))
            P.append(gf.path.arc(radius=radius, angle=-90))
            P.append(gf.path.straight(length=vertical_length))
            P.append(gf.path.arc(radius=radius, angle=-90))
            if i == spring_num - 1:
                P.append(gf.path.straight(length=horizontal_length))
                P.append(gf.path.arc(radius=radius, angle=90))
            else:
                P.append(gf.path.straight(length=horizontal_length + radius))
        else:
            P.append(gf.path.straight(length=horizontal_length + radius))
            P.append(gf.path.arc(radius=radius, angle=90))
            P.append(gf.path.straight(length=vertical_length))
            P.append(gf.path.arc(radius=radius, angle=90))
            if i == spring_num - 1:
                P.append(gf.path.straight(length=horizontal_length))
                P.append(gf.path.arc(radius=radius, angle=-90))
            else:
                P.append(gf.path.straight(length=horizontal_length + radius))
    P.append(gf.path.straight(length=vertical_path))
    return P


def single_spring_path_doubleside(
    spring_num=2,
    total_length=250,
    horizontal_length=30,
    vertical_length=6,
    radius=5,
    vertical_mid_length=10,
):
    # springs
    P1 = gf.Path()
    P2 = gf.Path()
    P_list = [P1, P2]
    # vertical paths
    vertical_path = (
        total_length
        - (
            spring_num * (vertical_length + 4 * radius)
            + (spring_num - 1) * vertical_mid_length
        )
    ) / 2
    for j in range(2):
        P = P_list[j]
        P.append(gf.path.straight(length=vertical_path))
        k = 1 if j == 0 else -1
        for i in range(spring_num):
            P.append(gf.path.arc(radius=radius, angle=90 * k))
            P.append(gf.path.straight(length=horizontal_length))
            P.append(gf.path.arc(radius=radius, angle=-90 * k))
            P.append(gf.path.straight(length=vertical_length))
            P.append(gf.path.arc(radius=radius, angle=-90 * k))
            P.append(gf.path.straight(length=horizontal_length))
            P.append(gf.path.arc(radius=radius, angle=90 * k))
            if i != spring_num - 1:
                P.append(gf.path.straight(length=vertical_mid_length))
    P.append(gf.path.straight(length=vertical_path))
    return P_list


def create_mid_structure_square(
    total_length=250,
    spring_num=3,
    horizontal_length=20,
    vertical_length=6,
    radius=5,
    vertical_mid_length=10,
):
    mid_struct = gf.Component()
    spring_single = gf.Component()
    spring = gf.Component()
    pad = gf.components.rectangle(size=(100, 100), layer=(9, 0))
    gold = gf.components.rectangle(size=(95, 95), layer=(11, 0))
    P = single_spring_path_doubleside(
        spring_num=spring_num,
        total_length=total_length,
        horizontal_length=horizontal_length,
        vertical_length=vertical_length,
        radius=radius,
        vertical_mid_length=vertical_mid_length,
    )
    # create the component
    if type(P) == list:
        (spring_single << gf.path.extrude(P[0], width=2, layer=(9, 0))).rotate(90)
        (spring_single << gf.path.extrude(P[1], width=2, layer=(9, 0))).rotate(90)
    else:
        (spring_single << gf.path.extrude(P, width=2, layer=(9, 0))).rotate(90)
    (spring << spring_single).move((-41, -300))
    (spring << spring_single).move((-41, -300)).dmirror_x(0)
    round_corner_left = round_corner(w1=6, w2=2, length=4, rotation=90, layer=(9, 0))
    round_corner_right = round_corner(w1=6, w2=2, length=4, rotation=90, layer=(9, 0))
    (spring << round_corner_left).move((-41, -300))
    (spring << round_corner_right).move((-41, -300)).dmirror_x(0)
    mid_struct << spring
    (mid_struct << spring).drotate(angle=-90, center=(0, 0))
    (mid_struct << spring).drotate(angle=90, center=(0, 0))
    (mid_struct << spring).dmirror_y(0)
    # add pads
    pad = gf.components.rectangle(size=(100, 100), layer=(9, 0))
    gold = gf.components.rectangle(size=(95, 95), layer=(11, 0))
    (mid_struct << pad).move((-50, -50))
    (mid_struct << gold).move((-47.5, -47.5))
    return mid_struct


def create_mid_structure_circle(
    spring_num=3,
    total_length=270,
    horizontal_length=20,
    vertical_length=6,
    radius=5,
    vertical_mid_length=10,
):
    mid_struct = gf.Component()
    spring_single = gf.Component()
    spring = gf.Component()
    pad = gf.components.circle(radius=31, layer=(9, 0))
    gold = gf.components.circle(radius=27.5, layer=(11, 0))
    P = single_spring_path_doubleside(
        spring_num=spring_num,
        total_length=total_length,
        horizontal_length=horizontal_length,
        vertical_length=vertical_length,
        radius=radius,
        vertical_mid_length=vertical_mid_length,
    )
    # create the component
    if type(P) == list:
        (spring << gf.path.extrude(P[0], width=2, layer=(9, 0))).rotate(90).movey(30)
        (spring << gf.path.extrude(P[1], width=2, layer=(9, 0))).rotate(90).movey(30)
    else:
        (spring << gf.path.extrude(P, width=2, layer=(9, 0))).rotate(90).movey(30)
    # round_corner_base = round_corner(w1=6, w2=2, length=4, rotation=90, layer=(9, 0))
    # (spring << round_corner_base).movey(-300)

    mid_struct << spring
    for i in range(8):
        angle = 360 / 8 * i
        (mid_struct << spring).rotate(angle=angle, center=(0, 0))
    mid_struct << pad
    mid_struct << gold
    return mid_struct


if __name__ == "__main__":
    mode = 1
    if mode == 0:
        mid_struct = create_mid_structure_square()
    else:
        mid_struct = create_mid_structure_circle()
    mid_struct.show()
