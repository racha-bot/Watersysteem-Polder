import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Titel en introductie
st.title("Polder Watersysteem Digital Twin")
st.write("""
Welkom bij de interactieve hiii simulatie van een polder watersysteem. 
Hier kun je parameters aanpassen en zien hoe het waterpeil verandert over tijd.
""")

# Sidebar voor gebruikersinvoer
st.sidebar.header("Gebruikersinvoer")
oppervlakte = st.sidebar.number_input("Oppervlakte (in hectare)", value=100.0, min_value=1.0)
verhard_percentage = st.sidebar.slider("Percentage verhard oppervlak", 0, 100, 30)
onverhard_percentage = 100 - verhard_percentage  # Automatisch berekend
neerslag = st.sidebar.slider("Dagelijkse neerslag (mm)", 0, 100, 20)
verdamping = st.sidebar.slider("Dagelijkse verdamping (mm)", 0, 50, 5)
gemaalcapaciteit = st.sidebar.number_input("Gemaalcapaciteit (mm/dag)", value=15, min_value=0)

# Simulatieparameters
dagen = 30  # Simulatie loopt 30 dagen
waterhoogte = [50]  # Startwaterhoogte in cm

# Simulatie
for dag in range(1, dagen + 1):
    regen = neerslag * (oppervlakte * verhard_percentage / 100) / 100  # Water van verhard oppervlak
    afvoer = verdamping + (gemaalcapaciteit if waterhoogte[-1] > 60 else 0)
    nieuw_peil = waterhoogte[-1] + regen - afvoer
    waterhoogte.append(max(nieuw_peil, 0))

# Grafiek visualisatie
st.header("Simulatie Resultaten")
fig, ax = plt.subplots()
ax.plot(range(dagen + 1), waterhoogte, label="Waterhoogte (cm)", color="blue")
ax.axhline(60, color="red", linestyle="--", label="Gemaaldrempel")
ax.set_title("Waterpeil over Tijd")
ax.set_xlabel("Dag")
ax.set_ylabel("Waterhoogte (cm)")
ax.legend()
ax.grid()

st.pyplot(fig)

# Kaart (Mock visualisatie)
st.header("Polder Kaart (Mockup)")
st.write("Hier kun je een kaart van de polder laten zien met hoogtes en waterniveaus.")
x, y = np.meshgrid(np.linspace(0, 10, 100), np.linspace(0, 10, 100))
hoogtekaart = np.sin(x) * np.cos(y) * 5 + 50  # Mock hoogte in cm
fig2, ax2 = plt.subplots()
im = ax2.imshow(hoogtekaart, cmap="viridis", origin="lower")
plt.colorbar(im, ax=ax2, label="Waterhoogte (cm)")
ax2.set_title("Waterhoogte Kaart")
ax2.set_xlabel("x (km)")
ax2.set_ylabel("y (km)")

st.pyplot(fig2)

# Toekomstige uitbreiding
st.header("Toekomstige Uitbreiding")
st.write("""
- Geavanceerdere kaarten en simulaties
- Koppeling met het wiskundige model
- Scenario's voor klimaatverandering en extreme weersomstandigheden
""")
