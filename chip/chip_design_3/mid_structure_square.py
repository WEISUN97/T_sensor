import gdsfactory as gf


def single_spring_path(spring_num=3, total_length=250):
    # springs
    P = gf.Path()
    # vertical paths
    vertical_length = (total_length - (spring_num * 8 + 4)) / 2
    P.append(gf.path.straight(length=vertical_length))

    for i in range(spring_num):
        if i % 2 == 0:
            if i == 0:
                P.append(gf.path.arc(radius=2, angle=90))
                P.append(gf.path.straight(length=20))
            else:
                P.append(gf.path.straight(length=22))
            P.append(gf.path.arc(radius=2, angle=-90))
            P.append(gf.path.straight(length=4))
            P.append(gf.path.arc(radius=2, angle=-90))
            if i == spring_num - 1:
                P.append(gf.path.straight(length=20))
                P.append(gf.path.arc(radius=2, angle=90))
            else:
                P.append(gf.path.straight(length=22))
        else:
            P.append(gf.path.straight(length=22))
            P.append(gf.path.arc(radius=2, angle=90))
            P.append(gf.path.straight(length=4))
            P.append(gf.path.arc(radius=2, angle=90))
            if i == spring_num - 1:
                P.append(gf.path.straight(length=20))
                P.append(gf.path.arc(radius=2, angle=-90))
            else:
                P.append(gf.path.straight(length=22))
    P.append(gf.path.straight(length=vertical_length))
    return P


def create_mid_structure_square(total_length=250, spring_num=3):
    mid_struct = gf.Component()
    spring_single = gf.Component()
    spring = gf.Component()
    pad = gf.components.rectangle(size=(100, 100), layer=(9, 0))
    gold = gf.components.rectangle(size=(95, 95), layer=(11, 0))
    P = single_spring_path(spring_num, total_length)
    # create the component
    (spring_single << gf.path.extrude(P, width=2, layer=(9, 0))).rotate(90)
    (spring << spring_single).move((-41, -300))
    (spring << spring_single).move((-41, -300)).dmirror_x(0)

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


def create_mid_structure_circle(total_length=270, spring_num=3):
    mid_struct = gf.Component()
    spring_single = gf.Component()
    spring = gf.Component()
    pad = gf.components.circle(radius=31, layer=(9, 0))
    gold = gf.components.circle(radius=27.5, layer=(11, 0))
    P = single_spring_path(spring_num, total_length)
    # create the component
    (spring << gf.path.extrude(P, width=2, layer=(9, 0))).rotate(90).movey(30)

    mid_struct << spring
    for i in range(8):
        angle = 360 / 8 * i
        (mid_struct << spring).rotate(angle=angle, center=(0, 0))
    mid_struct << pad
    mid_struct << gold
    return mid_struct


if __name__ == "__main__":
    mid_struct = create_mid_structure_square()
    mid_struct.show()


# def create_mid_structure_square(total_length=250, spring_num=3):
#     mid_struct = gf.Component()
#     pad = gf.components.rectangle(size=(100, 100), layer=(9, 0))
#     gold = gf.components.rectangle(size=(95, 95), layer=(11, 0))

#     # springs
#     spring_single = gf.Component()
#     spring = gf.Component()
#     spring_unit = gf.Component()
#     # vertical paths
#     vertical_length = (total_length - (spring_num * 8 + 2)) / 2
#     y1 = gf.components.rectangle(size=(2, vertical_length), layer=(9, 0))
#     # spring unit components (2 horizontal paths and 1 vertical path)
#     y2 = gf.components.rectangle(size=(2, 6), layer=(9, 0))
#     x1 = gf.components.rectangle(size=(26, 2), layer=(9, 0))
#     (spring_unit << x1).movex(-24)
#     (spring_unit << y2).move((-24, 2))
#     (spring_unit << x1).move((-24, 8))

#     spring_single << y1
#     for i in range(spring_num):
#         if i % 2 == 0:
#             (spring_single << spring_unit).move((0, vertical_length + i * 8))
#         else:
#             (spring_single << spring_unit).move((0, vertical_length + i * 8)).dmirror_x(
#                 1
#             )
#     (spring_single << y1).move((0, vertical_length + spring_num * 8 + 2))

#     (spring << spring_single).move((-41, -300))
#     (spring << spring_single).move((-41, -300)).dmirror_x(0)

#     mid_struct << spring
#     (mid_struct << spring).drotate(angle=-90, center=(0, 0))
#     (mid_struct << spring).drotate(angle=90, center=(0, 0))
#     (mid_struct << spring).dmirror_y(0)

#     (mid_struct << pad).move((-50, -50))
#     (mid_struct << gold).move((-47.5, -47.5))
#     return mid_struct
