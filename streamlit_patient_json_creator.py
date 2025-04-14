import streamlit as st
import json
import os

# Nom du fichier de sauvegarde
FICHIER_JSON = "dossiers_patients.json"

# Chargement des données existantes si disponibles
if os.path.exists(FICHIER_JSON):
    with open(FICHIER_JSON, "r", encoding="utf-8") as f:
        patients = json.load(f)
else:
    patients = []

# Initialisation de la session
if 'patients' not in st.session_state:
    st.session_state.patients = patients

st.title("Créateur de JSON pour entraînement GPT - Données patients")

st.markdown("""
Cette application vous permet de saisir des dossiers patients avec les éléments classiques d’un dossier d’urgence. 
Les données seront ensuite exportables en JSON pour entraîner un modèle GPT sur Azure.
""")

with st.form("patient_form"):
    st.subheader("Données d'entrée (Input pour l'I.A)")
    histoire = st.text_area("Histoire de la maladie")
    antecedents = st.text_area("Antécédents")
    traitements = st.text_area("Traitements habituels")
    motif = st.text_area("Motif de recours")
    constantes = st.text_area("Constantes")
    prescriptions = st.text_area("Prescriptions réalisées")
    observations = st.text_area("Observations des urgences")
    conclusion = st.text_area("Conclusion")

    st.subheader("Données de sortie (Target pour l'I.A)")
    valorisation = st.text_input("Valorisation")
    ccmu = st.text_input("CCMU")
    gemsa = st.text_input("GEMSA")
    cim10 = st.text_input("CIM10")
    ccam = st.text_input("CCAM")
    avis = st.text_input("Avis Spécialisé")

    submitted = st.form_submit_button("Ajouter le dossier")

    if submitted:
        dossier = {
            "input": {
                "Histoire de la maladie": histoire,
                "Antécédents": antecedents,
                "Traitements habituels": traitements,
                "Motif de recours": motif,
                "Constantes": constantes,
                "Prescriptions réalisées": prescriptions,
                "Observations des urgences": observations,
                "Conclusion": conclusion
            },
            "target": {
                "Valorisation": valorisation,
                "CCMU": ccmu,
                "GEMSA": gemsa,
                "CIM10": cim10,
                "CCAM": ccam,
                "Avis Spécialisé": avis
            }
        }
        st.session_state.patients.append(dossier)

        # Sauvegarde immédiate du fichier JSON
        with open(FICHIER_JSON, "w", encoding="utf-8") as f:
            json.dump(st.session_state.patients, f, indent=4, ensure_ascii=False)

        st.success("Dossier ajouté et sauvegardé avec succès.")

# Affichage du nombre de dossiers
st.info(f"Nombre de dossiers saisis : {len(st.session_state.patients)}")

# Bouton pour exporter en JSON
if st.session_state.patients:
    if st.button("Exporter en JSON"):
        with open(FICHIER_JSON, "r", encoding="utf-8") as f:
            json_data = f.read()
        st.download_button(
            label="Télécharger le JSON",
            data=json_data,
            file_name="dossiers_patients.json",
            mime="application/json"
        )
