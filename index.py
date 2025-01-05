import streamlit as st
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np

# Functie om 2D-coördinaten te extruderen naar 3D
def extrude_2d_to_3d(x, y, depth):
    front = [(x[i], y[i], 0) for i in range(len(x))]
    back = [(x[i], y[i], depth) for i in range(len(x))]
    return front, back

# Functie om een trapezium in 3D te tekenen
def draw_trapezoid_3d(ax, x, y, z, bottom_width, height, depth):
    bottom_width *= 2
    top_width = bottom_width + height

    left_bottom_front = (x - bottom_width / 2, y, z)
    right_bottom_front = (x + bottom_width / 2, y, z)
    left_top_front = (left_bottom_front[0] - height / 2, y + height, z)
    right_top_front = (right_bottom_front[0] + height / 2, y + height, z)

    left_bottom_back = (x - bottom_width / 2, y, z + depth)
    right_bottom_back = (x + bottom_width / 2, y, z + depth)
    left_top_back = (left_bottom_back[0] - height / 2, y + height, z + depth)
    right_top_back = (right_bottom_back[0] + height / 2, y + height, z + depth)

    vertices = [
        [left_bottom_front, right_bottom_front, right_top_front, left_top_front],
        [left_bottom_back, right_bottom_back, right_top_back, left_top_back],
        [left_bottom_front, left_top_front, left_top_back, left_bottom_back],
        [right_bottom_front, right_top_front, right_top_back, right_bottom_back],
        [left_top_front, right_top_front, right_top_back, left_top_back],
        [left_bottom_front, right_bottom_front, right_bottom_back, left_bottom_back],
    ]

    for face in vertices:
        ax.add_collection3d(Poly3DCollection([face], color='white', edgecolor='blue', alpha=0.7))

# Functie om de 3D-dijk te tekenen
def draw_dijk_3d(grondtype, hoogte, gemaal_capacity, werkuren):
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    depth = 10
    
    x_dijk = np.array([-3, -2.50, -1.5, -0.5, 0.5, 1, 1.5, 2.5, 3.5, 4, 8.5, 9, 10, 11, 11.5, 12, 13, 14, 15, 15.5]) * 2
    y_dijk = np.array([2, 5, 5, 3, 3, 4, 4, 2, 2, 3, 3, 2, 2, 4, 4, 3, 3, 5, 5, 2]) * 2
    
    front, back = extrude_2d_to_3d(x_dijk, y_dijk, depth)
    
    dijk_color = {"Zand": "yellow", "Klei": "blue", "Veen": "purple"}.get(grondtype, "brown")
    
    for i in range(len(front) - 1):
        vertices = [front[i], front[i + 1], back[i + 1], back[i]]
        ax.add_collection3d(Poly3DCollection([vertices], color=dijk_color, alpha=0.7))
    
    ax.add_collection3d(Poly3DCollection([front], color=dijk_color, alpha=0.5))
    ax.add_collection3d(Poly3DCollection([back], color=dijk_color, alpha=0.5))

    offset = 3
    draw_trapezoid_3d(ax, 3 - offset, 6, 0, 1, 1.5, depth)
    draw_trapezoid_3d(ax, 9 - offset, 4, 0, 1, hoogte, depth)
    draw_trapezoid_3d(ax, 16 + offset, 4, 0, 1, hoogte, depth)
    draw_trapezoid_3d(ax, 22 + offset, 6, 0, 1, 1.5, depth)
    
    ax.set_xlim(-5, 30)
    ax.set_ylim(0, 15)
    ax.set_zlim(-5, 15)

    ax.view_init(elev=100, azim=-90)
    st.pyplot(fig)

# Streamlit UI
st.title("3D Dijk Visualisatie")

grondtype = st.selectbox("Kies het grondtype:", ["Zand", "Klei", "Veen"])
neerslag = st.slider("Hoeveelheid neerslag (mm):", 0, 200, 50)
oppervlakte = st.number_input("Oppervlakte (m²):", value=1000, min_value=1)
gemaal_capacity = st.number_input("Capaciteit van het gemaal (m³/h):", value=10.0, min_value=0.0)
werkuren = st.number_input("Aantal werkuren van het gemaal:", value=10, min_value=0)

if st.button("Visualiseer Dijk"):
    draw_dijk_3d(grondtype, neerslag / 100, gemaal_capacity, werkuren)
