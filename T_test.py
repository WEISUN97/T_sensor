import gdsfactory as gf
from datetime import datetime

cell = gf.Component()

gap = 5
# Part 1 L=2000um
L = [2000]
w = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 2.0, 3.0, 4.0, 5.0]
for i in range(len(L)):
    for j in range(len(w)):
        beam = gf.components.rectangle(size=(L[i], w[j]), layer=(2, 0))
        beam_ref = cell << beam
        beam_ref.movey(20 * j)
        frame1 = gf.components.rectangle(size=(L[i], w[j] + 2 * gap), layer=(3, 0))
        frame1_ref = cell << frame1
        frame1_ref.movey(20 * j - gap)

        T = gf.components.text(f"{w[j]}", size=10, layer=(1, 0))
        T_ref1 = cell << T
        T_ref2 = cell << T
        T_ref1.move((-30, 20 * j - 5))
        T_ref2.move((L[i] + 10, 20 * j - 5))

T = gf.components.text(f"L=2000", size=20, layer=(1, 0))
T_ref = cell << T
T_ref.move((0, -50))

# Part 2 L=500um
L = [500]
w = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 2.0, 3.0, 4.0, 5.0]
for i in range(len(L)):
    for j in range(len(w)):
        beam = gf.components.rectangle(size=(L[i], w[j]), layer=(2, 0))
        beam_ref = cell << beam
        beam_ref.movey(-20 * (j + 5))

        frame2 = gf.components.rectangle(size=(L[i], w[j] + 2 * gap), layer=(3, 0))
        frame2_ref = cell << frame2
        frame2_ref.movey(-20 * (j + 5) - gap)

        T = gf.components.text(f"{w[j]}", size=10, layer=(1, 0))
        T_ref1 = cell << T
        T_ref2 = cell << T
        T_ref1.move((-30, -20 * (j + 5) - 5))
        T_ref2.move((L[i] + 10, -20 * (j + 5) - 5))

T2 = gf.components.text(f"L=500", size=20, layer=(1, 0))
T_ref = cell << T2
T_ref.move((0, -400))

# Part 3 L=1000um
L = [1000]
w = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 2.0, 3.0, 4.0, 5.0]

for i in range(len(L)):
    for j in range(len(w)):
        beam = gf.components.rectangle(size=(L[i], w[j]), layer=(2, 0))
        beam_ref = cell << beam
        beam_ref.move((640, -20 * (j + 5)))

        frame3 = gf.components.rectangle(size=(L[i], w[j] + 2 * gap), layer=(3, 0))
        frame3_ref = cell << frame3
        frame3_ref.move((640, -20 * (j + 5) - gap))

        T = gf.components.text(f"{w[j]}", size=10, layer=(1, 0))
        T_ref1 = cell << T
        T_ref2 = cell << T
        T_ref1.move((600, -20 * (j + 5) - 5))
        T_ref2.move((1640 + 10, -20 * (j + 5) - 5))

T3 = gf.components.text(f"L=1000", size=20, layer=(1, 0))
T_ref = cell << T3
T_ref.move((600, -400))

# frame1 = gf.components.rectangle(size=(2000, 285), layer=(3, 0))
# (cell << frame1).movey(-10)
# frame2 = gf.components.rectangle(size=(500, 280.1), layer=(3, 0))
# (cell << frame2).movey(-370)
# frame3 = gf.components.rectangle(size=(1000, 280.1), layer=(3, 0))
# (cell << frame3).move((640, -370))

beams = gf.boolean(
    A=cell, B=cell, operation="not", layer1=(3, 0), layer2=(2, 0), layer=(1, 0)
)
cell << beams
cell.flatten()
# cell.show()
suffix = datetime.now().strftime("%Y%m%d_%H")
cell.write_gds(f"T_test{suffix}.gds", write_context_info=False)
