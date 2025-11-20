
import streamlit as st
import pandas as pd
import os

# Fichier CSV pour sauvegarde
data_file = "historique_seances.csv"

# Charger ou initialiser les données
if os.path.exists(data_file):
    historique = pd.read_csv(data_file)
else:
    historique = pd.DataFrame(columns=["Jour", "Exercice", "Charge", "Séries faites"])

# Programme initial
program = {
    "Jour 1 - Abdos": [
        {"Exercice": "Crunch abdos à la poulie", "Reps": "3-4 x 12-15", "Charge": 25},
        {"Exercice": "Relevé jambes chaise romaine", "Reps": "3 x 10-12", "Charge": 0},
        {"Exercice": "Rotation poulie basse", "Reps": "3 x 12", "Charge": 10},
    ],
    "Jour 2 - Jambes": [
        {"Exercice": "Leg Curl allongé", "Reps": "4 x 12-15", "Charge": 30},
        {"Exercice": "Belt Squat", "Reps": "4 x 10-12", "Charge": 50},
        {"Exercice": "Fentes marchées", "Reps": "3 x 10", "Charge": 12},
    ],
    "Jour 3 - Abdos": [
        {"Exercice": "Relevé bassin au sol", "Reps": "3-4 x 12", "Charge": 0},
        {"Exercice": "Crunch SwissBall", "Reps": "3 x 15", "Charge": 0},
        {"Exercice": "Gainage frontal", "Reps": "3 x 30 sec", "Charge": 0},
    ],
    "Jour 4 - Jambes": [
        {"Exercice": "Presse 45°", "Reps": "4 x 12-15", "Charge": 80},
        {"Exercice": "Adducteurs machine", "Reps": "3 x 15-20", "Charge": 50},
        {"Exercice": "Abducteurs poulie", "Reps": "3 x 15", "Charge": 45},
    ],
}

# Interface
st.title("💪 Programme Femme - Suivi + Progression")
day = st.selectbox("📆 Choisis ton jour :", list(program.keys()))
st.subheader(day)

session_data = []

# Affichage
for i, ex in enumerate(program[day]):
    st.markdown(f"### {ex['Exercice']}")
    st.write(f"Répétitions : {ex['Reps']} | Charge actuelle : {ex['Charge']} kg")
    cols = st.columns(4)
    checks = [cols[j].checkbox(f"Série {j+1}", key=f"{day}_{i}_{j}") for j in range(4)]
    series_done = sum(checks)

    # Progression : augmenter la charge si 4/4 cochées
    new_charge = ex['Charge']
    if series_done == 4 and ex['Charge'] > 0:
        new_charge += 2  # +2 kg progression

    session_data.append({
        "Jour": day,
        "Exercice": ex['Exercice'],
        "Charge": new_charge,
        "Séries faites": series_done
    })

if st.button("💾 Sauvegarder ma séance"):
    new_df = pd.DataFrame(session_data)
    historique = pd.concat([historique, new_df], ignore_index=True)
    historique.to_csv(data_file, index=False)
    st.success("Séance sauvegardée avec progression !")

if st.checkbox("📈 Voir mon historique"):
    st.dataframe(historique)
